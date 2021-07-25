from typing import Any, Dict, List, Optional, Set, Union, Callable
from itertools import filterfalse
import re
from os import system, name, path
from colorama import init
from termcolor import colored
import pyperclip
from enum import IntEnum

from parser_types import (
    ComplexNode,
    PrimitiveNode,
    Structure,
    PlaintextInListItemScenario
)
from parser_is_start_of_x import (
    BAB_NUMBER_REGEX,
    BAB_NUMBER_WITH_OPEN_QUOTE_CHAR_REGEX,
    BAGIAN_NUMBER_REGEX,
    BAGIAN_NUMBER_WITH_OPEN_QUOTE_CHAR_REGEX,
    CLOSE_QUOTE_CHAR,
    LINE_ENDING_REGEXES,
    LIST_INDEX_DEFINITIONS,
    LIST_INDEX_STRUCTURES,
    OPEN_QUOTE_CHAR,
    PAGE_NUMBER_REGEX,
    PASAL_NUMBER_ALPHANUMERIC_VARIANT_REGEX,
    PASAL_NUMBER_REGEX,
    PASAL_NUMBER_WITH_OPEN_QUOTE_CHAR_REGEX,
    PENJELASAN_LIST_INDEX_DEFINITIONS,
    PENJELASAN_LIST_INDEX_REGEXES,
    PENJELASAN_PASAL_DEMI_PASAL_REGEX,
    START_OF_PERUBAHAN_SECTION_REGEXES,
    is_heading,
    is_start_of_bagian,
    is_start_of_first_list_index,
    is_start_of_list_index_str,
    is_start_of_paragraf,
    is_start_of_pasal,
    is_start_of_penjelasan,
    is_start_of_penjelasan_list_index_str,
    is_start_of_penjelasan_pasal_demi_pasal,
    is_start_of_perubahan_bab,
    is_start_of_perubahan_bagian,
    is_start_of_perubahan_pasal,
    is_start_of_structure,
    is_start_of_unordered_list_index_str,
)
from parser_ui import print_dashed_line, print_line, print_section_header, print_yes_no


class CleaningStageOrder(IntEnum):
    CLEAN_SQUASHED_PAGE_NUMBERS = 1
    CLEAN_MAYBE_LIST_ITEMS = 2
    CLEAN_MAYBE_SQUASHED_HEADINGS = 3
    CLEAN_SPLIT_PLAINTEXT = 4
    CLEAN_SPLIT_PASAL_NUMBER = 5
    INSERT_PERUBAHAN_QUOTES = 6


CLEANING_STAGES: Dict[CleaningStageOrder, Dict[str, List[str]]] = {
    CleaningStageOrder.CLEAN_SQUASHED_PAGE_NUMBERS:
        {
            'cleaned_law': []
        },
    CleaningStageOrder.CLEAN_MAYBE_LIST_ITEMS:
        {
            'cleaned_law': []
        },
    CleaningStageOrder.CLEAN_MAYBE_SQUASHED_HEADINGS:
        {
            'cleaned_law': []
        },
    CleaningStageOrder.CLEAN_SPLIT_PLAINTEXT:
        {
            'cleaned_law': []
        },
    CleaningStageOrder.CLEAN_SPLIT_PASAL_NUMBER:
        {
            'cleaned_law': []
        },
    CleaningStageOrder.INSERT_PERUBAHAN_QUOTES:
        {
            'cleaned_law': []
        }
}


def ignore_line(line: str) -> bool:
    """Checks if a line should be ignored during parsing. These lines are usually
    extra decorative content added to a PDF that isn't part of the law itself.
    Examples include page numbers e.g '5 / 23', '- 10 -'

    Args:
        line: string to be checked

    Returns:
        bool: True if line should be ignored, False otherwise

    Examples:
        >>> ignore_line('5 / 23')
        True

        >>> ignore_line('. . .')
        True

        >>> ignore_line('Mengingat bahwa regulasi minuman beralkohol...')
        False
    """
    # end of page
    if ". . ." in line:
        return True
    elif "www.hukumonline.com" in line:
        return True
    elif re.match(PAGE_NUMBER_REGEX, line.rstrip()) != None:
        return True
    # page number
    elif re.match(r'- [0-9]+ -', line.rstrip()) != None:
        return True
    elif line == '' or line.isspace():
        return True
    else:
        return False


def get_list_index_type(list_index_str: str) -> Structure:
    """Identify the type of list index in list_index_str

    Args:
        list_index_str: string that maybe represents a list index

    Returns:
        Optional[Structure]: the Structure enum that represents the type of list index,
        or None if no list index is in string

    Examples:
        >>> get_list_index_type('a.')
        Structure.LETTER_WITH_DOT

        >>> get_list_index_type('(2)')
        Structure.NUMBER_WITH_BRACKETS

        >>> get_list_index_type('3.')
        Structure.NUMBER_WITH_DOT

        >>> get_list_index_type('Ayat (4)')
        Structure.PENJELASAN_AYAT

        >>> get_list_index_type('Huruf e')
        Structure.PENJELASAN_HURUF

        >>> get_list_index_type('Angka 17')
        Structure.PENJELASAN_ANGKA

        >>> get_list_index_type('cara berpikir kreatif')
        None

        >>> get_list_index_type('a. cara berpikir kreatif')
        None
    """
    for structure, definition in LIST_INDEX_DEFINITIONS.items():
        regex = definition['regex']
        assert isinstance(regex, str)

        if is_heading(regex, list_index_str):
            return structure

    raise Exception(f'the string "{list_index_str}" is not a LIST_INDEX')


def get_list_index_as_num(list_index_str: str) -> int:
    """Get the numerical value represented by list_index_string

    Args:
        list_index_string: string that represents a list index

    Returns:
        int: the numerical value that represents list_index_string

    Examples:
        >>> get_list_index_as_num('d.')
        4

        >>> get_list_index_as_num('13.')
        13

        >>> get_list_index_as_num('Ayat (8)')
        8

        >>> get_list_index_as_num('Huruf d')
        4
    """
    structure = get_list_index_type(list_index_str)
    regex = LIST_INDEX_DEFINITIONS[structure]['regex']
    assert isinstance(regex, str)

    match = re.match(regex, list_index_str)
    # mypy: https://mypy.readthedocs.io/en/stable/common_issues.html#unexpected-errors-about-none-and-or-optional-types
    assert match is not None

    number_string = match.groupdict()['number']
    assert isinstance(number_string, str)

    # e.g '100'
    if number_string.isnumeric():
        return int(number_string)
    # e.g 'a'
    elif number_string.isalpha():
        return ord(number_string.lower())-96
    else:
        raise Exception(
            f'Invalid input {list_index_str}: note this function doesnt work on alphanumeric list indexes')


def is_alphanumeric_list_index(list_index_str: str) -> bool:
    for definition in LIST_INDEX_DEFINITIONS.values():
        regex = definition['regex']
        assert isinstance(regex, str)

        if not is_heading(regex, list_index_str):
            continue

        match = re.match(regex, list_index_str)
        if match == None:
            continue

        assert match is not None
        capture_groups = match.groupdict()

        if 'alphabet' not in capture_groups:
            continue

        if capture_groups['alphabet'] != '':
            return True

    return False


def is_next_list_index_number(list_index_a: str, list_index_b: str) -> bool:
    """Check if list_index_b is the next list index after list_index_a

    Args:
        list_index_a: string that represents a list index
        list_index_b: string that represents a list index

    Returns:
        bool: True if list_index_b is the next list index after list_index_a

    Examples:
        >>> is_next_list_index_number('d.', 'e.')
        True

        >>> is_next_list_index_number('(13)', '(14)')
        True

        >>> is_next_list_index_number('(13)', '(15)')
        False

        >>> is_next_list_index_number('a.', '(2)')
        Exception('next_list_index_number: Invalid input')
    """
    a_type = get_list_index_type(list_index_a)
    b_type = get_list_index_type(list_index_b)

    if b_type not in LIST_INDEX_STRUCTURES:
        raise Exception('next_list_index_number: Invalid input')
    if not (a_type == None or a_type == b_type):
        raise Exception('next_list_index_number: Invalid input')

    if is_alphanumeric_list_index(list_index_a) or is_alphanumeric_list_index(list_index_b):
        print_line()
        print(list_index_a)
        print_dashed_line()
        print(list_index_b)
        print_line()
        print('Are they consecutive list indexes?')
        print_yes_no()
        user_input = input()

        # user_input = 'y'
        if user_input == 'y':
            return True
        elif user_input == 'n':
            return False
        else:
            raise Exception('Invalid input; answer y or n')

    if a_type == None:
        return is_start_of_first_list_index(list_index_b)

    return get_list_index_as_num(list_index_a) + 1 == get_list_index_as_num(list_index_b)


def load_clean_law(filename: str) -> List[str]:
    should_clean_law = True
    clean_filename = f'{filename}-clean.txt'

    if path.isfile(clean_filename):
        y = colored('y', 'green')
        n = colored('n', 'red')
        print(
            f'{clean_filename} already exists. Do you want to use it?: {y} / {n} ? ')
        user_input = input()

        if user_input == 'y':
            should_clean_law = False

    law: List[str] = []
    if should_clean_law:
        file = open(
            filename + '.txt',
            mode='r',
            encoding='utf-8-sig')
        law = file.read().split("\n")
        law = clean_law(law)

        save_law_to_file(law, clean_filename)

    else:
        file = open(
            clean_filename,
            mode='r',
            encoding='utf-8-sig')
        law = file.read().split("\n")

    return law


def clean_law_at_stage(stage: int, law: List[str]) -> List[str]:
    '''
    Picks which function to use on law - a list implementation of a law document -
    based on user input on stage number (stage)

    Args:
        stage: user input on stage number which would determine the transformation on law
                based on the order in enum CleaningStageOrder
        law: ordered list of strings that contain the text of the law we want to parse

    Returns:
        List[str]: a modified list of strings from law based on which function was implemented
    '''
    if stage == CleaningStageOrder.CLEAN_SQUASHED_PAGE_NUMBERS.value:
        '''
        Remove _squashed_ semantically meaningless text e.g '. . .' or '1 / 23'

        Mostly, they come in whole lines, but sometimes they get squashed
        onto the end of real lines

        e.g a real line ending in '2 / 43' in UU 18 2017
        '''
        return clean_squashed_page_numbers(law)
    elif stage == CleaningStageOrder.CLEAN_MAYBE_LIST_ITEMS.value:
        '''
        Deal with list indexes. See clean_maybe_list_item for more.
        '''
        return clean_maybe_list_items(law)
    elif stage == CleaningStageOrder.CLEAN_MAYBE_SQUASHED_HEADINGS.value:
        '''
        Deal with heading structures (e.g PASAL_NUMBER) squashed onto the end of
        the previous line. (In theory, this can be expanded to BAB_TITLE, BAGIAN_TITLE etc.)
        '''
        return clean_maybe_squashed_headings(law)
    elif stage == CleaningStageOrder.CLEAN_SPLIT_PLAINTEXT.value:
        '''
        Stitch together plaintext lines that get separated into 2 lines due to page breaks
        '''
        return clean_split_plaintext(law)
    elif stage == CleaningStageOrder.CLEAN_SPLIT_PASAL_NUMBER.value:
        '''
        TODO(johnamadeo): Fix "Pasal 38 B" REMOVE THE SPACE WITH REGEX
        '''
        return clean_split_pasal_number(law)
    elif stage == CleaningStageOrder.INSERT_PERUBAHAN_QUOTES.value:
        '''
        Add OPEN_QUOTE_CHAR and CLOSE_QUOTE_CHAR to PERUBAHAN_SECTION and PENJELASAN_PERUBAHAN_SECTION
        '''
        return insert_perubahan_quotes(law)
    else:
        raise Exception(f'Unknown stage {stage}')


def clean_law(law: List[str]) -> List[str]:
    """Takes in a law (in the form of an ordered list of strings) and performs transformations
    that makes it easier to parse (while keeping it as a list of strings). The 2 transformations
    we do right now is to a) remove semantically meaningless lines (e.g a page number) and
    b) split up list items. See function implementation for more.

    Args:
        law: ordered list of strings that contain the text of the law we want to parse

    Returns:
        List[str]: the initial list of strings after transformations have been applied to it

    Examples:
        >>> clean_law(law = [
        ...     '1 / 10',
        ...     'Pasal 1',
        ...     '. . .',
        ...     'Dalam Undang-Undang in yang dimaksud dengan:',
        ...     '1. Informasi adalah keterangan',
        ... ])
        [
            'Pasal 1',
            'Dalam Undang-Undang in yang dimaksud dengan:',
            '1.',
            'Informasi adalah keterangan',
        ]
    """
    # TODO(johnamadeo): Make logic below a real stage?
    def clean_whitespace(l):
        return ' '.join(l.split())

    law = [line.strip() for line in law]
    law = [clean_whitespace(line) for line in law]

    new_law = []
    squashed_phrase = 'DENGAN RAHMAT TUHAN YANG MAHA ESA'
    for line in law:
        if line.endswith(squashed_phrase):
            new_law.extend([
                clean_whitespace(line.split(squashed_phrase)[0]),
                squashed_phrase,
            ])
            pass
        else:
            new_law.append(line)
    law = new_law

    '''
    Preps for cleaning stages saving mechanism
    TODO(Mel):  Extend saving mechanism to catch and save during a crash
    '''
    print_section_header("STARTING CLEANING")
    '''
    Remove semantically meaningless text e.g '. . .' or '1 / 23'
    This part only removes meaningless text that are not squashed
    onto the end of real lines.

    This is seperated from cleaning stages at it doesn't require user input.

    This work is continued on CleaningStageOrder.CLEAN_SQUASHED_PAGE_NUMBER
    '''
    law = list(filterfalse(ignore_line, law))

    next_cleaning_stage = 1
    len_cleaning_stage_order = len(CleaningStageOrder)
    pick_stage = '1'

    '''
    Saving mechanism is created to allow users to redo their inputs in
    specific stages in case there are wrong inputs without needing to redo 
    the entire cleaning stage from scratch.

    It works by giving an order to each cleaning stages (CleaningStageOrder)
    and saving each subsequent transformation on the previous law (ordered list of strings)
    into a dictionary in the stage order. With each stage passed, the user is prompted
    to say 'n' which would automatically choose the next stage, or to choose a number
    (int_pick_stage) based on stages that have passed.

    When a user goes back to a certain stage by choosing a number (x), all 
    resulting laws from x + 1 onwards are deleted to ensure order and consistency
    in results.

    These steps iterates until all stages are finished and the user explicitly
    gives consent to end the cleaning stages.

    The terminal will continuously ask for user input
    and stay in the cleaning stage until the next_cleaning_stage
    is bigger than the number of stages (len_cleaning_stage_order)

    This is to ensure that the user can go back to cleaning
    for possible revisions even if all cleaning stages have been completed.
    '''
    while next_cleaning_stage <= len_cleaning_stage_order:

        if next_cleaning_stage > 1:

            print_line()
            print("")
            print(colored('SAVED STAGES: ', 'blue'))
            for stage in CleaningStageOrder:
                if len(CLEANING_STAGES[stage]['cleaned_law']) == 0:
                    break
                print(f"{stage.value}. {stage.name}")
            print("")
            print_line()

            pick_number = colored('number', 'blue')
            pick_d = colored('d', 'blue')

            print(f"Pick a stage {pick_number} or")
            pick_stage = input(f"enter {pick_d} to go to the next stage: ")

        if pick_stage == 'd':
            '''Next cleaning stage depends on last cleaned stage'''
            print(f"next cleaning stage is {next_cleaning_stage}")
            pick_stage = str(next_cleaning_stage)

        elif not pick_stage.isnumeric():
            print("")
            print(
                f"{colored('Invalid input. Choose {pick_d} or a {pick_number}', 'red')}")
            continue

        int_pick_stage = int(pick_stage)
        current_stage = CLEANING_STAGES[CleaningStageOrder(int_pick_stage)]

        if int_pick_stage == 1:
            previous_stage = {'cleaned_law': law}
        else:
            previous_stage = CLEANING_STAGES[CleaningStageOrder(
                int_pick_stage - 1)]

        if int_pick_stage > len_cleaning_stage_order:
            print("")
            print(f"{colored('Invalid number. No stage with that number.', 'red')}")
            continue

        elif (int_pick_stage != 1 and len(previous_stage['cleaned_law']) == 0):
            '''
            Checks whether or not the previous stage from int_pick_stage has a valid law list
            If not, then the stage of int_pick_stage should not be implemented
            and the terminal should re-ask the user for input
            '''
            print("")
            print(
                f"{colored('Invalid stage number. All former stages must be cleaned first.', 'red')}")
            continue

        '''
        Uses clean_law_at_stage to find which function to implement
        Read documentation on clean_law_at_stage for more information
        '''
        if int_pick_stage in range(1, len_cleaning_stage_order + 1):
            try:
                current_stage['cleaned_law'] = clean_law_at_stage(
                    int_pick_stage, previous_stage['cleaned_law'])

                next_cleaning_stage = int_pick_stage + 1
            except:
                raise Exception(f'No logic for handling {current_stage}')

        else:
            raise ValueError("Invalid input.")

        if next_cleaning_stage > len_cleaning_stage_order:
            '''
            At this point all cleaning stages have passed.

            Explicit permission from user is needed to proceed to parsing.
            If user permission is not given, user is given a chance to
            redo any cleaning stage.
            '''
            print_section_header("Last cleaning stage finished")
            print("Proceed to parsing?")
            print("(y) to proceed to parsing.")
            print("(n) to undo to specific cleaning stages.")
            print_yes_no()

            finish_parsing = ''

            while finish_parsing not in ('y', 'n'):
                finish_parsing = input()
                if finish_parsing == 'y':
                    print(colored('Proceeding to parsing...', 'blue'))
                    next_cleaning_stage += 1
                elif finish_parsing == 'n':
                    print(colored('Going back to cleaning stages...', 'blue'))
                    next_cleaning_stage = len_cleaning_stage_order
                else:
                    print(colored('Invalid input.', 'red'))

        else:
            '''
            Deleting stage n + 1 and subsequent stages to eliminate the chance of
            double-cleaning/wrongful steps of cleaning
            '''
            for i in range(int_pick_stage + 1, len_cleaning_stage_order):
                CLEANING_STAGES[CleaningStageOrder(i)]['cleaned_law'].clear()

    return CLEANING_STAGES[CleaningStageOrder(len_cleaning_stage_order)]['cleaned_law']


def clean_split_pasal_number(law: List[str]) -> List[str]:
    new_law = []
    regex = r'(“?Pasal[\s]+[0-9]+[\s]+[A-Z])'

    for line in law:
        if is_heading(regex, line):
            pasal, number, letter = line.split()
            new_law.append(f'{pasal} {number}{letter}')
        else:
            new_law.append(line)

    return new_law


def insert_perubahan_section_open_quotes(law: List[str]) -> List[str]:
    new_law = []
    for line in law:
        new_law.append(line)

    # add open quote char in body
    for i, line in enumerate(new_law):
        if is_start_of_penjelasan(new_law, i):
            break

        if is_heading(PASAL_NUMBER_ALPHANUMERIC_VARIANT_REGEX, line) or\
                is_heading(BAB_NUMBER_REGEX, line) or \
                is_heading(BAGIAN_NUMBER_REGEX, line):

            print_line()
            print(f'[Line] {line}')
            if i + 1 < len(new_law):
                print_dashed_line()
                print(new_law[i+1])
            print_line()

            pyperclip.copy(line)
            print('Add open quote in front of line?')
            print_yes_no()
            user_input = input()

            if user_input == 'y':
                new_law[i] = OPEN_QUOTE_CHAR + line
            elif user_input != 'n':
                raise Exception(f'Invalid input {user_input}')

    return new_law


def insert_perubahan_section_close_quotes(law: List[str]) -> List[str]:
    new_law = []
    for line in law:
        new_law.append(line)

    # add close quote char in body
    open_quote_indexes: List[int] = []
    for i, line in enumerate(new_law):
        if is_start_of_penjelasan(new_law, i):
            break

        if any([is_heading(regex, line) for regex in START_OF_PERUBAHAN_SECTION_REGEXES]):
            open_quote_indexes.append(i)

    best_guess_index = -1
    for i, _ in enumerate(open_quote_indexes):
        open_quote_index = open_quote_indexes[i]
        if i == len(open_quote_indexes) - 1:
            next_open_quote_index = len(new_law)
        else:
            next_open_quote_index = open_quote_indexes[i+1]

        has_close_quote = False
        for j in range(open_quote_index, next_open_quote_index):
            if new_law[j][-1] == CLOSE_QUOTE_CHAR:
                has_close_quote = True
                break

        if has_close_quote:
            continue

        best_guess_index = next_open_quote_index-3
        print_line()
        for j in range(open_quote_index, next_open_quote_index):
            if j == best_guess_index:
                print(f"{colored(f'[Line {j}] {new_law[j]}', 'green')}")
            else:
                print(f'[Line {j}] {new_law[j]}')

            print_dashed_line()

        pyperclip.copy(new_law[open_quote_index])
        print('For which line should a close quote be added to the end?')
        if best_guess_index != -1:
            print(f'Or {colored("y(es)", "green")} to use the best guess line')

        user_input = input()

        user_input_int = -1
        if user_input == 'y':
            user_input_int = best_guess_index
        else:
            if not user_input.isnumeric():
                raise Exception(
                    f"Invalid input {user_input} - expected a number")

            user_input_int = int(user_input)
            if user_input_int < open_quote_index or user_input_int >= next_open_quote_index:
                print('This input may be out of bounds. Do you want to proceed?')
                print_yes_no()
                user_input = input()
                if user_input == 'y':
                    pass
                else:
                    raise Exception(
                        f"Invalid input {user_input} - out of bounds")

        new_law[user_input_int] = new_law[user_input_int] + CLOSE_QUOTE_CHAR

    return new_law


def insert_penjelasan_perubahan_section_open_quotes(law: List[str]) -> List[str]:
    new_law = []
    for line in law:
        new_law.append(line)

    open_quote_headings: Set[str] = set()
    for i, line in enumerate(new_law):
        if is_start_of_penjelasan(new_law, i):
            break

        if line[0] == OPEN_QUOTE_CHAR and \
            (is_start_of_perubahan_pasal(new_law, i) or
                is_start_of_perubahan_bab(new_law, i) or
                is_start_of_perubahan_bagian(new_law, i)):

            open_quote_headings.add(line[1:])

    in_penjelasan_pasal_demi_pasal = False
    for i, line in enumerate(new_law):
        if is_start_of_penjelasan_pasal_demi_pasal(new_law, i):
            in_penjelasan_pasal_demi_pasal = True

        if not in_penjelasan_pasal_demi_pasal:
            continue

        if line in open_quote_headings or \
                is_start_of_perubahan_pasal(new_law, i) or \
                is_start_of_perubahan_bab(new_law, i) or \
                is_start_of_perubahan_bagian(new_law, i):

            print()
            print_line()
            print(line)
            print_line()

            pyperclip.copy(line)
            print('Add open quote in front of line?')
            print_yes_no()
            user_input = input()

            if user_input == 'y':
                new_law[i] = OPEN_QUOTE_CHAR + line
            elif user_input != 'n':
                raise Exception(f'Invalid input {user_input}')

    return new_law


def insert_penjelasan_perubahan_section_close_quotes(law: List[str]) -> List[str]:
    new_law = []
    for line in law:
        new_law.append(line)

    # add close quote char in body
    open_quote_indexes: List[int] = []
    in_penjelasan_pasal_demi_pasal = False
    for i, line in enumerate(new_law):
        if is_start_of_penjelasan_pasal_demi_pasal(new_law, i):
            in_penjelasan_pasal_demi_pasal = True

        if not in_penjelasan_pasal_demi_pasal:
            continue

        if any([is_heading(regex, line) for regex in START_OF_PERUBAHAN_SECTION_REGEXES]):
            open_quote_indexes.append(i)

    for i, _ in enumerate(open_quote_indexes):
        open_quote_index = open_quote_indexes[i]
        if i == len(open_quote_indexes) - 1:
            next_open_quote_index = len(new_law)
        else:
            next_open_quote_index = open_quote_indexes[i+1]

        print()
        print()
        print_line()
        best_guess_index = -1
        for j in range(open_quote_index, next_open_quote_index):
            # heuristic for guessing which line to add close quote to
            if j+1 < len(law) and is_start_of_structure(Structure.PENJELASAN_ANGKA, new_law, j+1):
                best_guess_index = j
                print(f"{colored(f'[Line {j}] {new_law[j]}', 'green')}")
            else:
                print(f'[Line {j}] {new_law[j]}')

            print_dashed_line()

        pyperclip.copy(new_law[open_quote_index])
        print('For which line should a close quote be added to the end?')
        if best_guess_index != -1:
            print(f'Or {colored("y(es)", "green")} to use the best guess line')
        user_input = input()

        if user_input == 'y':
            if best_guess_index == -1:
                raise Exception(
                    'Invalid input - not best guess available to use')
            close_quote_index = best_guess_index
        elif not user_input.isnumeric():
            raise Exception(f"Invalid input {user_input} - expected a number")
        else:
            close_quote_index = int(user_input)
            if close_quote_index < open_quote_index or close_quote_index >= next_open_quote_index:
                print('This input may be out of bounds. Do you want to proceed?')
                print_yes_no()
                user_input = input()
                if user_input == 'y':
                    pass
                else:
                    raise Exception(
                        f"Invalid input {user_input} - out of bounds")

        new_law[close_quote_index] += CLOSE_QUOTE_CHAR

    return new_law


def insert_perubahan_quotes(law: List[str]) -> List[str]:
    print_section_header('INSERT PERUBAHAN SECTION QUOTES...')

    print('Is this UU an UU Perubahan?')
    print_yes_no()
    user_input = input()
    if user_input == 'n':
        return law
    elif user_input != 'y':
        raise Exception(f'Invalid input {user_input}')

    '''
    helper functions MUST be called in this order
    '''
    law = insert_perubahan_section_open_quotes(law)
    save_law_to_file(law, 'g1.txt')
    law = insert_perubahan_section_close_quotes(law)
    save_law_to_file(law, 'g2.txt')
    law = insert_penjelasan_perubahan_section_open_quotes(law)
    save_law_to_file(law, 'g3.txt')
    law = insert_penjelasan_perubahan_section_close_quotes(law)

    return law


def clean_squashed_page_numbers(law: List[str]) -> List[str]:
    print_section_header('CLEANING SQUASHED PAGE NUMBER...')

    new_law = []
    for idx, line in enumerate(law):
        result = re.split(PAGE_NUMBER_REGEX, line)
        if len(result) == 1:
            new_law.append(line)
        elif len(result) > 1:
            print_line()
            print(f'{idx} / {len(law)}')
            print(line)
            print_line()

            pyperclip.copy(line)
            print('Does this line have a page number squashed onto the end?')
            print_yes_no()
            user_input = input()

            # user_input = 'y'
            if user_input == 'y':
                new_law.append(''.join(result[:-2]))
            elif user_input == 'n':
                new_law.append(line)
            else:
                raise Exception(f'Input "{user_input}" is invalid')

    return new_law


def clean_split_plaintext(law: List[str]) -> List[str]:
    '''
    Stitch together plaintext lines that get separated into 2 lines due to page breaks
    '''
    print_section_header('CLEANING SPLIT PLAINTEXT...')

    new_law: List[str] = []
    for i, line in enumerate(law):
        '''
        the line length check is a heuristic to filter out false positives from the
        lowercase check due to list indexes e.g 'e.'

        The logic below is imprecise; it's just all heuristics & hands off to the user
        to make a decision
        '''
        really_long = len(law[i]) > 75
        long_enough = len(law[i]) > 5
        starts_with_lowercase = law[i][0].islower()
        starts_with_number = law[i][0].isnumeric()
        previous_line_long = i > 0 and len(law[i-1]) > 20
        previous_line_not_all_caps = i > 0 and not law[i-1].isupper()
        not_all_caps = not law[i].isupper()

        is_curr_line_maybe_split_plaintext = really_long or \
            (
                long_enough and (
                    starts_with_lowercase or
                    starts_with_number or
                    (
                        previous_line_long and
                        previous_line_not_all_caps and
                        not_all_caps and
                        not is_start_of_pasal(law, i) and
                        not is_start_of_perubahan_pasal(law, i) and
                        not is_start_of_penjelasan_list_index_str(law[i]) and
                        not is_start_of_bagian(law, i) and
                        not is_start_of_paragraf(law, i)
                    )
                )
            )

        is_prev_line_maybe_split_plaintext = i > 0 and len(law[i-1]) > 10

        if is_curr_line_maybe_split_plaintext and is_prev_line_maybe_split_plaintext:
            print('---------------------------------')
            print(f'{i} / {len(law)}')
            print(f'{law[i-1]}')
            print('- - - - - - - - - - - - - - - - -')
            print(f'{law[i]}')
            print('---------------------------------')

            pyperclip.copy(law[i])
            print("Combine lines into one?")
            print_yes_no()
            user_input = input()

            if user_input.lower() == 'y':
                new_law[-1] += (' '+line)
            else:
                new_law.append(line)
        else:
            new_law.append(line)

    return new_law


def clean_maybe_list_items(law: List[str]) -> List[str]:
    print_section_header('CLEANING MAYBE LIST ITEMS...')

    approx_len = len(law)
    new_law = []
    for idx, line in enumerate(law):
        list_item = clean_maybe_list_item(line, approx_len, idx)
        new_law.extend(list_item)

    return new_law


def clean_maybe_list_item(line: str, approx_len: int, approx_index: int) -> List[str]:
    """There are 2 transformations that we apply to clean lines that may have list items
    in the form that the parsing algorithm receives as a .txt

    a)
    In the .txt format this program usually receives the law in, every item
    in a list usually come in its own line (e.g '4. Ketentuan diubah sebagai berikut...')
    To make parsing later on easier, we want to split the line into '4.' and
    'Ketentuan diubah sebagai berikut...'. The general principle is that we want each line
    to be part of no more than 1 Primitive structure. If we had kept
    '4. Ketentuan diubah sebagai berikut...' in its original form, a substring of this single
    line would be a LIST_INDEX structure and another substring a PLAINTEXT structure.

    b)
    The law .txt that is fed into this program is usually converted from the original
    PDF. This conversion process is generally not perfect, so often what should be 2 (or more!)
    separate lines end up as a single line.

    e.g '(1) Setiap Orang berhak dilindungi hak-hak dasar. (2) Hak-hak yang dimaksud termasuk:'
    e.g Informasi Publik yang wajib disediakan adalah: a. asas dan tujuan;

    We want to fix these "squashed" lines to ensure the core parsing algorithm later on can
    assume the list of strings passed to it is correct (e.g every string truly represents
    a distinct line)

    Args:
        line: a line from the .txt the the parsing algorithm receives as input which
        may contain a list item

        approx_len: approximate no. of lines in law; used only for UI display to the user
        to show how far from the end of the law they are; the length is approximate 
        because this function itself will change the no. of lines in the law

        approx_idx: approximate line # currently being worked on; see approx_len

    Returns:
        List[str]: a list of strings whose content is basically the line argument split apart by
        the transformations described above have been mode

    Examples:
    """
    line_split = line.split()
    if is_start_of_list_index_str(line_split[0]) or \
            is_start_of_unordered_list_index_str(line_split[0]):
        return [
            line_split[0].strip(),
            *clean_maybe_list_item(' '.join(line_split[1:]), approx_len, approx_index)
        ]

    start_index = get_squashed_list_item(line, approx_len, approx_index)
    if start_index != None:
        return [
            line[:start_index-1].strip(),
            *clean_maybe_list_item(
                line[start_index:],
                approx_len,
                approx_index
            ),
        ]

    return [line.strip()]


def get_squashed_list_item(line: str, approx_len: int, approx_index: int):
    '''
    Find if line contains a squashed list item.

    Args:
        line: a line from the .txt the the parsing algorithm receives as input which
        may contain a list item

    Returns:
        Optional[int]: if line contains a list item, return the index at which the
        squashed list item starts

    Examples:
        >>> get_squashed_list_item('nasi goreng; 3. bakmie ayam;')
        13
    '''
    list_index_regexes = [r'(\u2212 )', r'(- )']
    for definition in LIST_INDEX_DEFINITIONS.values():
        regex = definition['regex']
        assert isinstance(regex, str)

        list_index_regexes.append(regex)

    regexes = []
    for i in LINE_ENDING_REGEXES:
        for j in list_index_regexes:
            regexes.append(i + r'\s+' + j)

    '''
    There may be multiple squashed list items on a single line; we want to identify
    the squashed list item that comes first. See parser_test for more details.
    '''
    earliest_match = None
    for regex in regexes:
        match = re.search(regex, line)
        if match is None:
            continue

        if (earliest_match is None) or match.start(0) < earliest_match.start(0):
            earliest_match = match

    if earliest_match is None:
        return None

    if 'full' not in earliest_match.groupdict():
        raise Exception(f'Cannot find start of list index in string "{line}"')

    start_of_squashed_list_item_idx = earliest_match.start('full')

    print_line()
    print(f'{approx_index} / {approx_len}')
    print(f'{line[:start_of_squashed_list_item_idx-1].strip()}')
    print_dashed_line()
    print(f'{line[start_of_squashed_list_item_idx:]}')
    print_line()

    pyperclip.copy(line[start_of_squashed_list_item_idx:])
    print('Split line?')
    print_yes_no()
    user_input = input()

    # user_input = 'y'
    if user_input == 'y':
        return start_of_squashed_list_item_idx
    else:
        return None


def clean_maybe_squashed_headings(law: List[str]) -> List[str]:
    print_section_header('CLEANING MAYBE SQUASHED HEADINGS...')

    approx_len = len(law)
    new_law = []
    for index, line in enumerate(law):
        list_item = clean_maybe_squashed_heading(line, approx_len, index)
        new_law.extend(list_item)

    return new_law


def clean_maybe_squashed_heading(line: str, approx_len: int, approx_index: int) -> List[str]:
    start_index = get_squashed_heading(line, approx_len, approx_index)
    if start_index != None:
        return [
            line[:start_index-1].strip(),
            *clean_maybe_squashed_heading(
                line[start_index:],
                approx_len,
                approx_index
            ),
        ]

    return [line.strip()]


def get_squashed_heading(line: str, approx_len: int, approx_index: int):
    heading_regex = [
        PASAL_NUMBER_REGEX,
        PASAL_NUMBER_WITH_OPEN_QUOTE_CHAR_REGEX,
        BAB_NUMBER_REGEX,
        BAB_NUMBER_WITH_OPEN_QUOTE_CHAR_REGEX,
        BAGIAN_NUMBER_REGEX,
        BAGIAN_NUMBER_WITH_OPEN_QUOTE_CHAR_REGEX,
        PENJELASAN_PASAL_DEMI_PASAL_REGEX,
        *PENJELASAN_LIST_INDEX_REGEXES,
    ]

    regexes = []
    for i in LINE_ENDING_REGEXES:
        for j in heading_regex:
            regexes.append(i + r'\s+' + j)

    '''
    There may be multiple squashed headings on a single line; we want to identify
    the squashed heading that comes first.
    '''
    earliest_match = None
    for regex in regexes:
        match = re.search(regex, line)
        if match is None:
            continue

        if (earliest_match is None) or match.start(0) < earliest_match.start(0):
            earliest_match = match

    if earliest_match is None:
        return None

    start_of_squashed_heading_idx = earliest_match.start(2)

    rest_of_line = line[start_of_squashed_heading_idx:]

    if len(rest_of_line) > 200:
        return None

    if not any([is_heading(regex, rest_of_line) for regex in heading_regex]):
        return None

    print_line()
    print(f'{approx_index} / {approx_len}')
    print(f"{line[:start_of_squashed_heading_idx-1].strip()}")
    print_dashed_line()
    print(f"{line[start_of_squashed_heading_idx:]}")
    print_line()

    pyperclip.copy(line[start_of_squashed_heading_idx:])
    print('Split line?')
    print_yes_no()
    user_input = input()

    # user_input = 'n'
    if user_input == 'y':
        return start_of_squashed_heading_idx
    else:
        return None


def print_around(law: List[str], i: int) -> None:
    """Prints law[start_index] and the lines right before & after it. Usually
    called before throwing an exception to provide more context.

    Args:
        law: ordered list of strings that contain the text of the law we want to parse
        i:

    Returns:

    Examples:
    """
    print(f'''
Below are lines {i} and the lines right before & after
--------------
{law[i-1] if i > 0 else '[NO PREVIOUS LINE]'}
{law[i]}
{law[i+1] if (i+1) < len(law) else '[NO NEXT LINE]'}
--------------
    ''')


def convert_tree_to_json(node: Union[ComplexNode, PrimitiveNode], ketentuan_umum_list: List[str]) -> Dict[str, Any]:
    if isinstance(node, PrimitiveNode):
        if get_parent_node(node, Structure.BAB) is not None and node.type == Structure.PLAINTEXT:
            for title in ketentuan_umum_list:
                index = node.text.upper().find(title)

                pasal_node = get_parent_node(node, Structure.PASAL)
                is_definition = get_id(pasal_node) == 'pasal-1'

                if is_word_part_of_text(node.text, title, index) and not is_definition:
                    text = node.text[index:index+len(title)]
                    '''
                    Determine if the word is actually a part of a bigger definition, 
                        and if such case happens, opt for the longer word

                    Ex: 
                    assume "Lorem ipsum" and "ipsum" exist in the dictionary

                    "Lorem ipsum dolor sit amet" -> "${Lorem ipsum} dolor sit amet"
                    "Ipsum dolor sit amet" -> "${Ipsum} dolor sit amet"
                    "Lorem ipsum ipsum lorem" -> "${Lorem ipsum} ${ipsum} lorem"
                    '''
                    match = re.findall(
                        r'\$\{[^\}]*' + text + '[^\$]*\}', node.text)
                    is_part_of_other_definition = len(match) > 0

                    if not is_part_of_other_definition:
                        node.text = node.text.replace(text, f'${{{text}}}')

        return {
            'type': node.type.value,
            'text': node.text,
        }
    else:
        return {
            'type': node.type.value,
            'id': get_id(node),
            'children': [convert_tree_to_json(child, ketentuan_umum_list) for child in node.children],
        }


def get_parent_node(node: Union[ComplexNode, PrimitiveNode], structure: Structure):
    if node.parent:
        if node.parent.type == structure:
            return node.parent

        return get_parent_node(node.parent, structure)

    return None


def is_word_part_of_text(string: str, substring: str, start_index) -> bool:
    '''
    Determine if a given substring is an independent word that's part of a text.
    Independent word means that the word is not a substring of another word

    This function checks whether the substring is surrounded by non-alphabet

    e.g.
    ("anak anak", "anak") -> true
    ("melaksanakan", "anak") -> false
    ("kami harus melaksanakan", "anak") -> false
    '''
    if start_index >= 0:
        end_index = start_index + len(substring)
        return ((start_index == 0 or not string[start_index-1].isalpha())
                and (end_index == len(string) or not string[end_index].isalpha()))

    return False


def extract_metadata_from_tree(undang_undang_node: ComplexNode) -> Dict[str, Any]:
    '''
    Extract important metadata about the law
    - Undang Undang number, year, and topic
    - Lembaran Negara number & year
    - Tambahan Lembaran Negara number

    A faster way would be to extract the metadata while parsing. But this approach
    provides 1 centralized place to see what all the metadata fields are + avoids
    adding another global variable during parsing.
    '''
    metadata: Dict[str, Any] = {
        'lembaranNegaraNumber': -1,
        'lembaranNegaraYear': -1,
        'tambahanLembaranNumber': -1,
        'number': -1,
        'topic': '',
        'year': -1,
    }

    '''
    the last line in the whole law is the no. of the Tambahan Lembaran Negara
    e.g TAMBAHAN LEMBARAN NEGARA REPUBLIK INDONESIA NOMOR 4279
    '''
    def f(node: Union[ComplexNode, PrimitiveNode]):
        child = node.children[-1]

        if isinstance(child, PrimitiveNode):
            # remove the Tambahan Lembaran Negara number from Penjelasan Umum
            node.children.pop()
            extractTLN(child)
            return

        f(child)

    def extractTLN(node: PrimitiveNode):
        match = re.search(r'([0-9]+)', node.text)
        if match is None:
            raise Exception('Failed to get Tambahan Lembaran Negara no.')

        metadata['tambahanLembaranNumber'] = int(match.group(0))

    f(undang_undang_node)

    def g(node: Union[ComplexNode, PrimitiveNode]):
        if isinstance(node, ComplexNode):
            for child in node.children:
                g(child)
        elif isinstance(node, PrimitiveNode):
            if node.type == Structure.UU_TITLE_YEAR_AND_NUMBER:
                match = re.search(r'NOMOR ([0-9]+) TAHUN ([0-9]+)', node.text)
                if match is None:
                    raise Exception('Failed to get UU year & no.')
                metadata['number'] = int(match.group(1))
                metadata['year'] = int(match.group(2))
            elif node.type == Structure.UU_TITLE_TOPIC:
                metadata['topic'] = capitalize(node.text)
            elif node.type == Structure.LEMBARAN_NUMBER:
                match = re.search(r'TAHUN ([0-9]+) NOMOR ([0-9]+)', node.text)
                if match is None:
                    raise Exception('Failed to get Lembaran Negara year & no.')
                metadata['lembaranNegaraYear'] = int(match.group(1))
                metadata['lembaranNegaraNumber'] = int(match.group(2))

    g(undang_undang_node)

    ketentuan_umum: Dict[str, Any] = {}

    def parse_ketentuan_umum(node: Union[ComplexNode, PrimitiveNode]):
        if not node.children:
            return

        if len(node.children) <= 2:
            for child in node.children:
                if isinstance(child, PrimitiveNode) and child.type == Structure.PLAINTEXT:
                    definition_text = child.text.split(r'adalah')

                    title = definition_text[0].strip()
                    definition = definition_text[1].strip()

                    if 'yang selanjutnya disebut' in title:
                        title = title.split(r' yang selanjutnya disebut ')[
                            1].strip(' ,')
                    if 'yang selanjutnya disingkat' in title:
                        title = title.split(r' yang selanjutnya disingkat ')[
                            1].strip(' ,')

                    ketentuan_umum[title.upper()] = definition
        else:
            title = None
            definition_list = []

            for child in node.children:
                if child.type == Structure.PLAINTEXT:
                    title = child.text.split(r'adalah')[0].strip()

                    if 'yang selanjutnya disebut' in title:
                        title = title.split(r' yang selanjutnya disebut ')[
                            1].strip(' ,')
                    if 'yang selanjutnya disingkat' in title:
                        title = title.split(r' yang selanjutnya disingkat ')[
                            1].strip(' ,')

                elif child.type == Structure.LIST:
                    for list_item in child.children:
                        definition = " ".join(
                            [node.text for node in list_item.children])
                        definition_list.append(definition)

            ketentuan_umum[title.upper()] = "\n".join(definition_list)

        metadata['ketentuan_umum'] = ketentuan_umum

    def h(node: Union[ComplexNode, PrimitiveNode]):
        if isinstance(node, ComplexNode):
            if node.parent and get_id(node.parent) == 'pasal-1':
                for child in node.children:
                    parse_ketentuan_umum(child)
            else:
                for child in node.children:
                    h(child)

    # TODO @willemchua: uncomment this after ketentuam umum parsing works on most edge cases
    # h(undang_undang_node)

    return metadata


def capitalize(string: str) -> str:
    '''
    Examples:
        >>> capitalize('PERLINDUNGAN KONSUMEN')
        'Perlindungan Konsumen'
    '''
    return ' '.join(
        [word[0].upper() + word[1:].lower()
         for word in string.strip().split(' ')]
    )


def roman_to_int(roman_numeral: str) -> int:
    """Converts string of a roman numeral to the integer the roman numeral represents
    Logic taken from https://www.w3resource.com/python-exercises/class-exercises/python-class-exercise-2.php

    Args:
        roman_numeral: a string of a roman numeral e.g 'VI', 'LIV'

    Returns:
        int: the integer value of roman_numeral e.g 6, 54

    Examples:
        >>> roman_to_int('IV')
        4
    """
    roman_values = {'I': 1, 'V': 5, 'X': 10,
                    'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    integer = 0
    for i in range(len(roman_numeral)):
        if i > 0 and roman_values[roman_numeral[i]] > roman_values[roman_numeral[i - 1]]:
            integer += roman_values[roman_numeral[i]] - \
                2 * roman_values[roman_numeral[i - 1]]
        else:
            integer += roman_values[roman_numeral[i]]
    return integer


def get_id(node: ComplexNode) -> str:
    if node.type == Structure.BAB:
        bab_number_node = node.children[0]
        assert isinstance(bab_number_node, PrimitiveNode) and \
            bab_number_node.type == Structure.BAB_NUMBER

        bab_number_roman = bab_number_node.text.split()[1]
        bab_number_int = roman_to_int(bab_number_roman)
        return f'bab-{str(bab_number_int)}'

    elif node.type == Structure.PASAL or node.type == Structure.PERUBAHAN_PASAL:
        pasal_number_node = node.children[0]
        assert isinstance(pasal_number_node, PrimitiveNode) and \
            pasal_number_node.type == Structure.PASAL_NUMBER

        pasal_number = pasal_number_node.text.split()[1]

        is_in_penjelasan = is_x_an_ancestor(
            node, Structure.PENJELASAN_PASAL_DEMI_PASAL)

        if node.type == Structure.PASAL:
            return f'pasal-{pasal_number}'
        elif node.type == Structure.PENJELASAN_PASAL:
            return f'penjelasan-pasal-{pasal_number}'
        elif node.type == Structure.PERUBAHAN_PASAL:
            return f'perubahan-pasal-{pasal_number}'
        elif node.type == Structure.PENJELASAN_PERUBAHAN_PASAL:
            return f'penjelasan-perubahan-pasal-{pasal_number}'

    elif node.type == Structure.BAGIAN:
        bagian_number_node = node.children[0]
        assert isinstance(bagian_number_node, PrimitiveNode) and \
            bagian_number_node.type == Structure.BAGIAN_NUMBER

        bagian_number_indo = bagian_number_node.text.split()[1].lower()
        '''
        Bagian numbers are mostly in the format of 'kesatu', 'kedua', etc.
        however on rare occasions the 1st bagian can be 'pertama' instead
        of 'kesatu'
        '''
        bagian_number_int: int = -1
        if bagian_number_indo == 'pertama':
            bagian_number_int = 1
        else:
            text = bagian_number_node.text
            bagian_number_indo = ' '.join(text.split()[1:])[2:].lower()
            """
            This is obviously janky, but good enough for now. When this fails,
            all we need to do is add more numbers and rerun the parser.
            """
            bagian_number_int = {
                'satu': 1,
                'dua': 2,
                'tiga': 3,
                'empat': 4,
                'lima': 5,
                'enam': 6,
                'tujuh': 7,
                'delapan': 8,
                'sembilan': 9,
                'sepuluh': 10,
                'sebelas': 11,
                'dua belas': 12,
                'duabelas': 12,
                'tiga belas': 13,
                'tigabelas': 13,
                'empat belas': 14,
                'empatbelas': 14,
                'lima belas': 15,
                'limabelas': 15,
                'enam belas': 16,
                'enambelas': 16,
                'tujuh belas': 17,
                'tujuhbelas': 17,
                'delapan belas': 18,
                'delapanbelas': 18,
                'sembilan belas': 19,
                'sembilanbelas': 19,
                'dua puluh': 20,
                'dua puluh satu': 21,
                'dua puluh dua': 22,
                'dua puluh tiga': 23,
                'dua puluh empat': 24,
                'dua puluh lima': 25,
                'dua puluh enam': 26,
                'dua puluh tujuh': 27,
                'dua puluh delapan': 28,
                'dua puluh sembilan': 29,
            }[bagian_number_indo]

        bab_node = node.parent
        assert isinstance(bab_node, ComplexNode) and \
            bab_node.type == Structure.BAB

        return f'{get_id(bab_node)}-bagian-{bagian_number_int}'

    elif node.type == Structure.PARAGRAF:
        paragraf_number_node = node.children[0]
        assert isinstance(paragraf_number_node, PrimitiveNode) and \
            paragraf_number_node.type == Structure.PARAGRAF_NUMBER

        bagian_node = node.parent
        assert isinstance(bagian_node, ComplexNode) and \
            bagian_node.type == Structure.BAGIAN

        bab_node = bagian_node.parent
        assert isinstance(bab_node, ComplexNode) and \
            bab_node.type == Structure.BAB

        return f'{get_id(bab_node)}-{get_id(bagian_node)}-paragraf-{paragraf_number_node.text.split()[1]}'

    elif node.type == Structure.PENJELASAN:
        return 'penjelasan'

    return ''


def gen_plaintext_in_list_item_scenario_from_user(law: List[str], i: int) -> PlaintextInListItemScenario:
    print_line()
    print(f'{law[i-2]}')
    print_dashed_line()
    print(f'{law[i-1]}')
    print_line()
    print()
    print(f'{law[i]}')
    print_line()

    pyperclip.copy(law[i])
    print('This line is the 3rd line of a LIST_INDEX. Is it:')
    print('- a sibling of the LIST this LIST_ITEM is in? (s)')
    print('- a PLAINTEXT child of the LIST ITEM? (c)')
    print('- a FORMATTED_MATH_ROW child of the LIST ITEM? (cm)')

    user_input = input()

    user_input = user_input.lower()
    if user_input == 's':
        return PlaintextInListItemScenario.SIBLING_OF_LIST
    elif user_input == 'c':
        return PlaintextInListItemScenario.CHILD_OF_LIST_ITEM
    elif user_input == 'cm':
        return PlaintextInListItemScenario.FORMATTED_MATH_ROW_CHILD_OF_LIST_ITEM
    else:
        raise Exception(f'Invalid command "{user_input}" entered by user')


def is_x_an_ancestor(
    node: Union[ComplexNode, PrimitiveNode],
    ancestor_structure: Structure
):
    if node.parent is not None:
        if node.parent.type == ancestor_structure:
            return True
        else:
            return is_x_an_ancestor(node.parent, ancestor_structure)

    return False


def get_perubahan_section_end_index(
    law: List[str],
    perubahan_section_start_index: int
) -> int:
    index = perubahan_section_start_index
    while index < len(law) - 1:
        '''
        TODO(@johnamadeo) May need some heuristics. What if line naturally has open quote & close quotes for
        another reason?
        '''
        if law[index][-1] == CLOSE_QUOTE_CHAR:
            return index

        index += 1

    raise Exception('Cannot find PERUBAHAN_SECTION end index')


def clean_perubahan_section_quotes(perubahan_section_node: ComplexNode):
    '''
    Remove open & close quotes at start & end of PERUBAHAN_SECTION
    '''
    def f(node: Union[ComplexNode, PrimitiveNode]):
        if isinstance(node, PrimitiveNode):
            return node
        else:
            return f(node.children[0])

    first_primitive_node = f(perubahan_section_node)
    first_primitive_node.text = first_primitive_node.text[1:]

    def g(node: Union[ComplexNode, PrimitiveNode]):
        if isinstance(node, PrimitiveNode):
            return node
        else:
            return g(node.children[-1])

    last_primitive_node = g(perubahan_section_node)
    last_primitive_node.text = last_primitive_node.text[:-1]


def save_law_to_file(law: List[str], filename: str):
    with open(filename, 'w') as outfile:
        txt_law = []
        for i, line in enumerate(law):
            if i < len(law) - 1:
                txt_law.append(f'{line}\n')
            else:
                txt_law.append(f'{line}')
        outfile.writelines(txt_law)
