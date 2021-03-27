from typing import Any, Dict, List, Optional, Union
from itertools import filterfalse
import re

from parser_types import (
    ComplexNode,
    PrimitiveNode,
    Structure,
    LIST_INDEX_STRUCTURES,
)
from parser_is_start_of_x import (
    is_start_of_number_with_brackets_str,
    is_start_of_number_with_dot_str,
    is_start_of_letter_with_dot_str,
    is_start_of_first_list_index,
    is_start_of_list_index_str
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
    elif re.match(r'[0-9]+ \/ [0-9]+', line.rstrip()) != None:
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

        >>> get_list_index_type('cara berpikir kreatif')
        None

        >>> get_list_index_type('a. cara berpikir kreatif')
        None
    """
    if is_start_of_number_with_brackets_str(list_index_str):
        return Structure.NUMBER_WITH_BRACKETS
    elif is_start_of_number_with_dot_str(list_index_str):
        return Structure.NUMBER_WITH_DOT
    elif is_start_of_letter_with_dot_str(list_index_str):
        return Structure.LETTER_WITH_DOT
    else:
        return None


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
    """
    regex = None
    if is_start_of_number_with_brackets_str(list_index_str):
        regex = r'\(([0-9]+)\)'
    elif is_start_of_number_with_dot_str(list_index_str):
        regex = r'([0-9]+)\.'
    elif is_start_of_letter_with_dot_str(list_index_str):
        regex = r'([a-z])\.'
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
    This function is not the most robust right now, because it doesn't
    handle alphanumeric edge cases (e.g how would it handle '1', '2a', '2b')

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

    if a_type == None:
        return is_start_of_first_list_index(list_index_b)

    return get_list_index_as_num(list_index_a) + 1 == get_list_index_as_num(list_index_b)


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
    Remove semantically meaningless lines e.g '. . .' or '1 / 23'
    '''
    law = list(filterfalse(ignore_line, law))

    '''
    Deal with list indexes. See clean_maybe_list_item for more.
    '''
    new_law = []
    for i, line in enumerate(law):
        list_item = clean_maybe_list_item(line)
        new_law.extend(list_item)

    return new_law


def clean_maybe_list_item(line: str) -> List[str]:
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

    Returns:
        List[str]: a list of strings whose content is basically the line argument split apart by
        the transformations described above have been mode

    Examples:
    """
    line_split = line.split()
    if is_start_of_list_index_str(line_split[0]):
        return [
            line_split[0].strip(),
            *clean_maybe_list_item(' '.join(line_split[1:]))
        ]

    start_index = get_squashed_list_item(line)
    if start_index != None:
        return [
            line[:start_index-1].strip(),
            *clean_maybe_list_item(line[start_index:]),
        ]

    return [line.strip()]


def get_squashed_list_item(line):
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
    line_ending_regex = [r'(;)', r'(:)', r'(\.)', r'(; dan/atau)']
    list_index_regex = [r'([a-z]\. )', r'([0-9]+\. )', r'(\([0-9]+\) )']
    for i in line_ending_regex:
        for j in list_index_regex:
            match = re.search(i + r'\s+' + j, line)
            if match != None:
                start_of_squashed_list_item_idx = match.start(2)
                print(match.groups())
                return start_of_squashed_list_item_idx
    return None


def get_next_list_index(list_index: str) -> str:
    """Returns the string of the next list index that comes after the list index passed in

    Args:
        list_index: string that represents a LIST_INDEX e.g 'a.', '(1)'

    Returns:
        str: string that represents the next LIST_INDEX

    Examples:
        >>> get_next_list_index(1, Structure.NUMBER_WITH_DOT)
        '2.'

        >>> get_next_list_index(1, Structure.NUMBER_WITH_BRACKETS)
        '(2)'

        >>> get_next_list_index(1, Structure.LETTER_WITH_DOT)
        'b.'
    """
    list_index_num = get_list_index_as_num(list_index)
    list_index_type = get_list_index_type(list_index)

    if list_index_num < 1 or list_index_type == None:
        raise Exception(f'argument is an invalid list index: {list_index}')

    if list_index_type == Structure.NUMBER_WITH_DOT:
        return f'{list_index_num+1}.'
    elif list_index_type == Structure.NUMBER_WITH_BRACKETS:
        return f'({list_index_num+1})'
    elif list_index_type == Structure.LETTER_WITH_DOT:
        return f'{chr(96+list_index_num+1)}.'
    else:
        raise Exception(
            f'{list_index_type} is not a list index Structure type')


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
{law[i-1] if i > 0 else ''}
{law[i]}
{law[i+1]}
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

    elif node.type == Structure.PASAL:
        pasal_number_node = node.children[0]
        assert isinstance(pasal_number_node, PrimitiveNode) and \
            pasal_number_node.type == Structure.PASAL_NUMBER

        return f'pasal-{pasal_number_node.text.split()[1]}'

    elif node.type == Structure.BAGIAN:
        bagian_number_node = node.children[0]
        assert isinstance(bagian_number_node, PrimitiveNode) and \
            bagian_number_node.type == Structure.BAGIAN_NUMBER

        bagian_number_indo = \
            bagian_number_node.text.split()[1][2:]
        """
        This is obviously janky, but good enough for now. When this fails,
        all we need to do is add more numbers and rerun the parser.
        """
        bagian_number_int: int = {
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

    return ''


def print_law(law: List[str]) -> None:
    for i, l in enumerate(law):
        print(f'[{i}] {l}\n')
