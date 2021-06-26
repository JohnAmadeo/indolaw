from typing import Any, Dict, List, Optional, Set, Union
from itertools import filterfalse
import re
from os import system, name, path
from colorama import init
from termcolor import colored

from parser_types import (
    ComplexNode,
    PrimitiveNode,
    Structure,
    LIST_INDEX_STRUCTURES,
    PlaintextInListItemScenario
)
from parser_is_start_of_x import (
    BAB_NUMBER_REGEX,
    BAB_NUMBER_WITH_OPEN_QUOTE_CHAR_REGEX,
    BAGIAN_NUMBER_REGEX,
    BAGIAN_NUMBER_WITH_OPEN_QUOTE_CHAR_REGEX,
    CLOSE_QUOTE_CHAR,
    LETTER_WITH_DOT_REGEX,
    LINE_ENDING_REGEXES,
    NUMBER_WITH_BRACKETS_ALPHANUMERIC_VARIANT_REGEX,
    NUMBER_WITH_BRACKETS_REGEX,
    NUMBER_WITH_DOT_ALPHANUMERIC_VARIANT_REGEX,
    NUMBER_WITH_DOT_REGEX,
    NUMBER_WITH_RIGHT_BRACKET_REGEX,
    OPEN_QUOTE_CHAR,
    PAGE_NUMBER_REGEX,
    PASAL_NUMBER_ALPHANUMERIC_VARIANT_REGEX,
    PASAL_NUMBER_REGEX,
    PASAL_NUMBER_WITH_OPEN_QUOTE_CHAR_REGEX,
    PENJELASAN_ANGKA_REGEX,
    PENJELASAN_AYAT_ALPHANUMERIC_VARIANT_REGEX,
    PENJELASAN_AYAT_REGEX,
    PENJELASAN_HURUF_REGEX,
    PENJELASAN_PASAL_DEMI_PASAL_REGEX,
    START_OF_PERUBAHAN_SECTION_REGEXES,
    is_heading,
    is_start_of_number_with_brackets_str,
    is_start_of_number_with_right_bracket_str,
    is_start_of_number_with_dot_str,
    is_start_of_letter_with_dot_str,
    is_start_of_first_list_index,
    is_start_of_list_index_str,
    is_start_of_pasal,
    is_start_of_penjelasan,
    is_start_of_penjelasan_angka,
    is_start_of_penjelasan_angka_str,
    is_start_of_penjelasan_ayat_str,
    is_start_of_penjelasan_huruf_str,
    is_start_of_penjelasan_list_index_str,
    is_start_of_penjelasan_pasal_demi_pasal,
    is_start_of_perubahan_bab,
    is_start_of_perubahan_bagian,
    is_start_of_perubahan_pasal,
    is_start_of_unordered_list_index_str,
)


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
    else:
        return False


def get_list_index_type(list_index_str: str) -> Optional[Structure]:
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
    if is_start_of_number_with_brackets_str(list_index_str):
        return Structure.NUMBER_WITH_BRACKETS
    elif is_start_of_number_with_right_bracket_str(list_index_str):
        return Structure.NUMBER_WITH_RIGHT_BRACKET
    elif is_start_of_number_with_dot_str(list_index_str):
        return Structure.NUMBER_WITH_DOT
    elif is_start_of_letter_with_dot_str(list_index_str):
        return Structure.LETTER_WITH_DOT
    elif is_start_of_penjelasan_ayat_str(list_index_str):
        return Structure.PENJELASAN_AYAT
    elif is_start_of_penjelasan_huruf_str(list_index_str):
        return Structure.PENJELASAN_HURUF
    elif is_start_of_penjelasan_angka_str(list_index_str):
        return Structure.PENJELASAN_ANGKA
    else:
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

        >>> get_list_index_as_num('(8)')
        8

        >>> get_list_index_as_num('Ayat (8)')
        8

        >>> get_list_index_as_num('Huruf d')
        4
    """
    regex = None
    if is_start_of_number_with_brackets_str(list_index_str):
        regex = r'\(([0-9]+)\)'
    elif is_start_of_number_with_right_bracket_str(list_index_str):
        regex = r'([0-9]+)\)'
    elif is_start_of_number_with_dot_str(list_index_str):
        regex = r'([0-9]+)[a-z]?\.'
    elif is_start_of_letter_with_dot_str(list_index_str):
        regex = r'([a-z])\.'
    elif is_start_of_penjelasan_huruf_str(list_index_str):
        regex = r'Huruf ([a-z])'
    elif is_start_of_penjelasan_ayat_str(list_index_str):
        regex = r'Ayat \(([0-9]+)\)'
    elif is_start_of_penjelasan_angka_str(list_index_str):
        regex = r'Angka ([0-9]+)'
    else:
        raise Exception('list_index_str is not a list index')

    match = re.match(regex, list_index_str)
    # mypy: https://mypy.readthedocs.io/en/stable/common_issues.html#unexpected-errors-about-none-and-or-optional-types
    assert match is not None

    number_string = match.group(1)
    # e.g '100'
    if number_string.isnumeric():
        return int(number_string)
    # e.g 'a'
    else:
        return ord(number_string.lower())-96


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

    if b_type not in set(LIST_INDEX_STRUCTURES):
        raise Exception('next_list_index_number: Invalid input')
    if not (a_type == None or a_type == b_type):
        raise Exception('next_list_index_number: Invalid input')

    if is_heading(NUMBER_WITH_DOT_ALPHANUMERIC_VARIANT_REGEX, list_index_a) or \
            is_heading(NUMBER_WITH_DOT_ALPHANUMERIC_VARIANT_REGEX, list_index_b) or \
            is_heading(NUMBER_WITH_BRACKETS_ALPHANUMERIC_VARIANT_REGEX, list_index_a) or \
            is_heading(NUMBER_WITH_BRACKETS_ALPHANUMERIC_VARIANT_REGEX, list_index_b) or \
            is_heading(PENJELASAN_AYAT_ALPHANUMERIC_VARIANT_REGEX, list_index_a) or \
            is_heading(PENJELASAN_AYAT_ALPHANUMERIC_VARIANT_REGEX, list_index_b):

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
    clean_filename = f'{filename}_clean.txt'

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

        with open(filename + '_clean.txt', 'w') as outfile:
            txt_law = []
            for i, line in enumerate(law):
                if i < len(law) - 1:
                    txt_law.append(f'{line}\n')
                else:
                    txt_law.append(f'{line}')
            outfile.writelines(txt_law)

    else:
        file = open(
            clean_filename,
            mode='r',
            encoding='utf-8-sig')
        law = file.read().split("\n")

    return law


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
    '''
    Remove semantically meaningless text e.g '. . .' or '1 / 23'

    Mostly, they come in whole lines, but sometimes they get squashed
    onto the end of real lines

    e.g a real line ending in '2 / 43' in UU 18 2017
    '''
    law = list(filterfalse(ignore_line, law))
    law = clean_squashed_page_numbers(law)

    '''
    Deal with list indexes. See clean_maybe_list_item for more.
    '''
    law = clean_maybe_list_items(law)

    '''
    Deal with heading structures (e.g PASAL_NUMBER) squashed onto the end of
    the previous line. (In theory, this can be expanded to BAB_TITLE, BAGIAN_TITLE etc.)
    '''
    law = clean_maybe_squashed_headings(law)

    '''
    Stitch together plaintext lines that get separated into 2 lines due to page breaks
    '''
    law = clean_split_plaintext(law)

    '''
    TODO(johnamadeo): Fix "Pasal 38 B" REMOVE THE SPACE WITH REGEX
    '''
    law = clean_split_pasal_number(law)

    '''
    Add OPEN_QUOTE_CHAR and CLOSE_QUOTE_CHAR to PERUBAHAN_SECTION and PENJELASAN_PERUBAHAN_SECTION
    '''
    law = insert_perubahan_quotes(law)

    law = [line.strip() for line in law]
    law = [' '.join(line.split()) for line in law]
    return law


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

        print_line()
        for j in range(open_quote_index, next_open_quote_index):
            print(f'[Line {j}] {new_law[j]}')
            print_dashed_line()
        print('For which line should a close quote be added to the end?')
        user_input = input()

        if not user_input.isnumeric():
            raise Exception(f"Invalid input {user_input} - expected a number")

        user_input_int = int(user_input)
        if user_input_int < open_quote_index or user_input_int >= next_open_quote_index:
            raise Exception(f"Invalid input {user_input} - out of bounds")

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

        if line in open_quote_headings:
            new_law[i] = OPEN_QUOTE_CHAR + new_law[i]
        elif is_start_of_perubahan_pasal(new_law, i) or \
                is_start_of_perubahan_bab(new_law, i) or \
                is_start_of_perubahan_bagian(new_law, i):

            print()
            print_line()
            print(line)
            print_line()
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
            if j+1 < len(law) and is_start_of_penjelasan_angka(new_law, j+1):
                best_guess_index = j
                print(f"{colored(f'[Line {j}] {new_law[j]}', 'green')}")
            else:
                print(f'[Line {j}] {new_law[j]}')

            print_dashed_line()

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
                raise Exception(f"Invalid input {user_input} - out of bounds")

        new_law[close_quote_index] += CLOSE_QUOTE_CHAR

    return new_law


def insert_perubahan_quotes(law: List[str]) -> List[str]:
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
    law = insert_perubahan_section_close_quotes(law)
    law = insert_penjelasan_perubahan_section_open_quotes(law)
    law = insert_penjelasan_perubahan_section_close_quotes(law)

    return law


def clean_squashed_page_numbers(law: List[str]) -> List[str]:
    print(f"{colored('---------------', 'green')}")
    print()
    print(f"{colored('CLEANING SQUASHED PAGE NUMBER...', 'green')}")
    print()
    print(f"{colored('---------------', 'green')}")

    new_law = []
    for idx, line in enumerate(law):
        result = re.split(PAGE_NUMBER_REGEX, line)
        if len(result) == 1:
            new_law.append(line)
        elif len(result) > 1:
            # remove page number at end of string
            print('---------------')
            print(f'{idx} / {len(law)}')
            print(line)
            print('---------------')

            print('Does this line have a page number squashed onto the end?')
            print_yes_no()
            user_input = input()

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
    print(f"{colored('---------------', 'green')}")
    print()
    print(f"{colored('CLEANING SPLIT PLAINTEXT...', 'green')}")
    print()
    print(f"{colored('---------------', 'green')}")

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
                        not is_start_of_penjelasan_list_index_str(law[i])
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
    print(f"{colored('---------------', 'green')}")
    print()
    print(f"{colored('CLEANING MAYBE LIST ITEMS...', 'green')}")
    print()
    print(f"{colored('---------------', 'green')}")

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
    def wrap_in_brackets_with_space(regex):
        return r'(' + regex + r' )'

    list_index_regex = [
        wrap_in_brackets_with_space(LETTER_WITH_DOT_REGEX),
        wrap_in_brackets_with_space(NUMBER_WITH_DOT_REGEX),
        wrap_in_brackets_with_space(NUMBER_WITH_BRACKETS_REGEX),
        wrap_in_brackets_with_space(NUMBER_WITH_RIGHT_BRACKET_REGEX),
    ]

    unordered_list_index_regex = [r'(\u2212 )', r'(- )']
    penjelasan_list_index_regex = [
        PENJELASAN_HURUF_REGEX,
        PENJELASAN_AYAT_REGEX,
        PENJELASAN_ANGKA_REGEX,
    ]

    regexes = []
    for i in LINE_ENDING_REGEXES:
        for j in list_index_regex + unordered_list_index_regex + penjelasan_list_index_regex:
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

    start_of_squashed_list_item_idx = earliest_match.start(2)

    print('---------------')
    print(f'{approx_index} / {approx_len}')
    print(f'{line[:start_of_squashed_list_item_idx-1].strip()}')
    print('- - - - - - - -')
    print(f'{line[start_of_squashed_list_item_idx:]}')
    print('---------------')
    print('Split line?')
    print_yes_no()
    user_input = input()

    if user_input == 'y':
        return start_of_squashed_list_item_idx
    else:
        return None


def clean_maybe_squashed_headings(law: List[str]) -> List[str]:
    print(f"{colored('---------------', 'green')}")
    print()
    print(f"{colored('CLEANING MAYBE SQUASHED HEADINGS...', 'green')}")
    print()
    print(f"{colored('---------------', 'green')}")

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
        PENJELASAN_PASAL_DEMI_PASAL_REGEX,
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

    print('---------------')
    print(f'{approx_index} / {approx_len}')
    print(f"{line[:start_of_squashed_heading_idx-1].strip()}")
    print('- - - - - - - -')
    print(f"{line[start_of_squashed_heading_idx:]}")
    print('---------------')
    print('Split line?')
    print_yes_no()
    user_input = input()

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


def convert_tree_to_json(node: Union[ComplexNode, PrimitiveNode]) -> Dict[str, Any]:
    if isinstance(node, PrimitiveNode):
        return {
            'type': node.type.value,
            'text': node.text,
        }
    else:
        return {
            'type': node.type.value,
            'id': get_id(node),
            'children': [convert_tree_to_json(child) for child in node.children],
        }


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
            bagian_number_indo = \
                bagian_number_node.text.split()[1][2:]
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


def print_law(law: List[str]) -> None:
    for i, l in enumerate(law):
        print(f'[{i}] {l}\n')


def clear():
    # i.e Windows
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')


def print_line():
    print('---------------')


def print_dashed_line():
    print('- - - - - - - -')


def print_yes_no():
    print(f"{colored('y', 'green')} / {colored('n', 'red')}")


def gen_plaintext_in_list_item_scenario_from_user(law: List[str], i: int) -> PlaintextInListItemScenario:
    print_line()
    print(f'{law[i-2]}')
    print_dashed_line()
    print(f'{law[i-1]}')
    print_line()
    print()
    print(f'{law[i]}')
    print_line()

    print('This PLAINTEXT is the 3rd line of a LIST_INDEX. Is it:')
    print('- a sibling of the LIST this LIST_ITEM is in? (s)')
    print('- a child of the LIST ITEM? (c)')
    print('- an embedded structure e.g is this UU modifying other UU? (e)')

    user_input = input()

    user_input = user_input.lower()
    if user_input == 's':
        return PlaintextInListItemScenario.SIBLING_OF_LIST
    elif user_input == 'c':
        return PlaintextInListItemScenario.CHILD_OF_LIST_ITEM
    elif user_input == 'e':
        return PlaintextInListItemScenario.EMBEDDED_LAW_SNIPPET
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
