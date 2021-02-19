from typing import List, Optional, Union
from itertools import filterfalse
import re

from parser_types import (
    Structure,
    Primitive,
    Complex,
    LIST_INDEX_STRUCTURES,
)
from parser_is_start_of_x import (
    is_start_of_number_with_brackets_str,
    is_start_of_number_with_dot_str,
    is_start_of_letter_with_dot_str,
    is_start_of_first_list_index,
    is_start_of_list_index,
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


def node(
    structure: Structure,
    children_list: List[Union[Primitive, Complex]],
    id: Optional[str] = '',
) -> Complex:
    # TODO(johnamadeo): This is just a placeholder for what should eventually become a proper Class constructor
    return {
        'type': structure.value,
        # this is to create a unique ID that can be used for HTML links
        'id': id,
        'children': children_list,
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
    elif re.match('[0-9]+ \/ [0-9]+', line.rstrip()) != None:
        return True
    # page number
    elif re.match('- [0-9]+ -', line.rstrip()) != None:
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
        regex = '\(([0-9]+)\)'
    elif is_start_of_number_with_dot_str(list_index_str):
        regex = '([0-9]+)\.'
    elif is_start_of_letter_with_dot_str(list_index_str):
        regex = '([a-z])\.'
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
    b) split up list items so that the list index & text block component are separate strings

    Args:
        law: ordered list of strings that represents a law

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
    law = list(filterfalse(ignore_line, law))

    new_law = []
    for i, line in enumerate(law):
        # if line has a list index e.g '4. Ketentuan diubah sebagai berikut'
        # we want to process it into 2 separate lines: '4.' and 'Ketentuan diubah sebagai berikut'
        # this makes parsing for LIST_ITEM and LIST_INDEX more convenient later on
        if is_start_of_list_index(law, i):
            line_split = line.split()
            new_law.append(line_split[0])
            new_law.append(' '.join(line_split[1:]))
        else:
            new_law.append(line)

    return new_law
