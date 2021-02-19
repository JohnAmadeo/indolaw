from parser_types import Structure
from parser_utils import (
    roman_to_int,
    ignore_line,
    get_list_index_type,
    get_list_index_as_num,
    is_next_list_index_number,
    clean_law
)
from parser_is_start_of_x import is_heading
import pytest


def test_roman_to_int():
    assert roman_to_int('VI') == 6
    assert roman_to_int('XXI') == 21
    assert roman_to_int('LIV') == 54


def test_is_heading():
    assert is_heading('BAB [0-9]+', '  BAB 23   ')
    assert not is_heading('BAB [0-9]+', 'dengan BAB 23   ')
    assert not is_heading('BAB [0-9]+', '  asdf   ')


def test_ignore_line():
    assert ignore_line('. . .')
    assert ignore_line('5 / 23')
    assert ignore_line('- 12 -')
    assert ignore_line('www.hukumonline.com')
    assert not ignore_line('Mengingat bahwa UU No. 14...')


def test_get_list_index_type():
    assert get_list_index_type('a.') == Structure.LETTER_WITH_DOT
    assert get_list_index_type('(2)') == Structure.NUMBER_WITH_BRACKETS
    assert get_list_index_type('3.') == Structure.NUMBER_WITH_DOT
    assert get_list_index_type('cara berpikir kreatif') == None
    assert get_list_index_type('a. cara berpikir kreatif') == None


def test_get_list_index_as_num():
    assert get_list_index_as_num('d.') == 4
    assert get_list_index_as_num('13.') == 13
    assert get_list_index_as_num('(8)') == 8
    with pytest.raises(Exception):
        get_list_index_as_num('Berhubungan dengan peraturan...')


def test_is_next_list_index_number():
    assert is_next_list_index_number('d.', 'e.') == True
    assert is_next_list_index_number('(13)', '(14)') == True
    assert is_next_list_index_number('(13)', '(15)') == False
    with pytest.raises(Exception):
        is_next_list_index_number('a.', '(2)')


def test_clean_law():
    input = [
        '1 / 10',
        'Pasal 1',
        '. . .',
        'Dalam Undang-Undang in yang dimaksud dengan:',
        '1. Informasi adalah keterangan',
    ]
    output = [
        'Pasal 1',
        'Dalam Undang-Undang in yang dimaksud dengan:',
        '1.',
        'Informasi adalah keterangan',
    ]
    assert clean_law(input) == output
