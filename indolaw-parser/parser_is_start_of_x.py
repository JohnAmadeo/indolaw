from typing import Dict, List, Union
import re
from parser_types import ListIndexDefinition, Structure
from parser_ui import print_line, print_yes_no
import pyperclip


def group(regex, name):
    return fr'(?P<{name}>{regex})'


OPEN_QUOTE_CHAR = '“'
CLOSE_QUOTE_CHAR = '”'

PASAL_NUMBER_REGEX = r'(Pasal[\s]+([0-9]+[A-Z]*|[MDCLXVI]+))'
PASAL_NUMBER_ALPHANUMERIC_VARIANT_REGEX = r'(Pasal[\s]+([0-9]+[A-Z]*))'
PASAL_NUMBER_WITH_OPEN_QUOTE_CHAR_REGEX = r'(“Pasal[\s]+([0-9]+[A-Z]*|[MDCLXVI]+))'
BAB_NUMBER_REGEX = r'(BAB [MDCLXVI]+[A-Z]*)'
BAB_NUMBER_WITH_OPEN_QUOTE_CHAR_REGEX = r'(“BAB [MDCLXVI]+[A-Z]*)'
BAGIAN_NUMBER_REGEX = r'(Bagian (Ke[a-z]+( (Belas|Puluh( [A-z][a-z]+)?))?|Pertama))'
BAGIAN_NUMBER_WITH_OPEN_QUOTE_CHAR_REGEX = r'(“Bagian (Ke[a-z]+( (Belas|Puluh( [A-z][a-z]+)?))?|Pertama))'
PARAGRAF_NUMBER_REGEX = r'(Paragraf[\s]+([0-9]+|Satu|Dua|Tiga|Empat|Lima|Enam|Tujuh|Delapan|Sembilan))'

PAGE_NUMBER_REGEX = r'([0-9]+[\s]*\/[\s]*[0-9]+)'

PLUS_OR_MINUS_REGEX = group(r' \((-|\+)\)', 'plus_or_minus')
CURRENCY_REGEX = group(r'Rp\.?\s*[0-9]+(\.[0-9]{3})+,00', 'currency')
CURRENCY_WITH_PLUS_MINUS_REGEX = fr'({CURRENCY_REGEX}(\.?|{PLUS_OR_MINUS_REGEX}?))'
FORMATTED_MATH_ROW_SPLIT_REGEX = group(
    fr'(=\s*)?{CURRENCY_WITH_PLUS_MINUS_REGEX}$', 'full')

PENJELASAN_PASAL_DEMI_PASAL_REGEX = r'((II\.? )?((PENJELASAN )?PASAL DEMI PASAL|Pasal Demi Pasal))'

LINE_ENDING_REGEXES = [
    r'(;)',
    r'(:)',
    r'(\.)',
    r'(; dan/atau)',
    r'(; dan)',
    r'(; atau)',
    r'(,)',
    r'(' + CLOSE_QUOTE_CHAR + r')'
]

START_OF_PERUBAHAN_SECTION_REGEXES = [
    PASAL_NUMBER_WITH_OPEN_QUOTE_CHAR_REGEX,
    BAB_NUMBER_WITH_OPEN_QUOTE_CHAR_REGEX,
    BAGIAN_NUMBER_WITH_OPEN_QUOTE_CHAR_REGEX,
]

ALPHANUMERIC_NUMBER_ALPHABET = group(fr'[a-zA-Z]?', 'alphabet')
ALPHANUMERIC_NUMBER = group(fr'[0-9]+{ALPHANUMERIC_NUMBER_ALPHABET}', 'number')
ALPHABET_NUMBER = group(fr'[a-z]', 'number')

'''
When adding a new list index:
(1) The 'regex' field must have the following named capture groups:
    - full: should capture the whole list index
    - number: should capture the numeric part of the list index e.g '4a' in '(4a)'
'''
LIST_INDEX_DEFINITIONS: Dict[Structure, ListIndexDefinition] = {
    Structure.LETTER_WITH_DOT:
        {
            'regex': group(fr'{ALPHABET_NUMBER}\.', 'full'),
            'is_penjelasan_list_index': False,
            'first_list_index': 'a.',
        },
    Structure.LETTER_WITH_BRACKETS:
        {
            'regex': group(fr'\({ALPHABET_NUMBER}\)', 'full'),
            'is_penjelasan_list_index': False,
            'first_list_index': '(a)',
        },
    Structure.LETTER_WITH_RIGHT_BRACKET:
        {
            'regex': group(fr'{ALPHABET_NUMBER}\)', 'full'),
            'is_penjelasan_list_index': False,
            'first_list_index': 'a)',
        },
    Structure.NUMBER_WITH_BRACKETS:
        {
            'regex': group(fr'\({ALPHANUMERIC_NUMBER}\)', 'full'),
            'is_penjelasan_list_index': False,
            'first_list_index': '(1)',
        },
    Structure.NUMBER_WITH_RIGHT_BRACKET:
        {
            'regex': group(fr'{ALPHANUMERIC_NUMBER}\)', 'full'),
            'is_penjelasan_list_index': False,
            'first_list_index': '1)',
        },
    Structure.NUMBER_WITH_DOT:
        {
            'regex': group(fr'{ALPHANUMERIC_NUMBER}\.', 'full'),
            'is_penjelasan_list_index': False,
            'first_list_index': '1.',
        },
    Structure.PENJELASAN_AYAT:
        {
            'regex': group(fr'Ayat \({ALPHANUMERIC_NUMBER}\)', 'full'),
            'is_penjelasan_list_index': True,
            'first_list_index': 'Ayat (1)',
        },
    Structure.PENJELASAN_HURUF:
        {
            'regex': group(fr'Huruf {ALPHABET_NUMBER}', 'full'),
            'is_penjelasan_list_index': True,
            'first_list_index': 'Huruf a',
        },
    Structure.PENJELASAN_ANGKA:
        {
            'regex': group(fr'Angka {ALPHANUMERIC_NUMBER}', 'full'),
            'is_penjelasan_list_index': True,
            'first_list_index': 'Angka 1',
        },
    Structure.PENJELASAN_ANGKA_WITH_RIGHT_BRACKET:
        {
            'regex': group(fr'Angka {ALPHANUMERIC_NUMBER}\)', 'full'),
            'is_penjelasan_list_index': True,
            'first_list_index': 'Angka 1)',
        }
}

PENJELASAN_LIST_INDEX_DEFINITIONS = {
    k: v for k, v in LIST_INDEX_DEFINITIONS.items() if v['is_penjelasan_list_index'] == True}

PENJELASAN_LIST_INDEX_REGEXES: List[str] = []
for definition in PENJELASAN_LIST_INDEX_DEFINITIONS.values():
    regex = definition['regex']
    assert isinstance(regex, str)
    PENJELASAN_LIST_INDEX_REGEXES.append(regex)

LIST_INDEX_STRUCTURES = set(LIST_INDEX_DEFINITIONS.keys())
NORMAL_LIST_INDEX_STRUCTURES = set(filter(
    lambda s: LIST_INDEX_DEFINITIONS[s]['is_penjelasan_list_index'] == False,
    LIST_INDEX_DEFINITIONS.keys()
))
PENJELASAN_LIST_INDEX_STRUCTURES = set(filter(
    lambda s: LIST_INDEX_DEFINITIONS[s]['is_penjelasan_list_index'] == True,
    LIST_INDEX_DEFINITIONS.keys()
))

FIRST_LIST_INDEXES = set([e['first_list_index']
                         for e in LIST_INDEX_DEFINITIONS.values()])


def is_start_of_structure(structure: Structure, law: List[str], start_index: int) -> bool:
    """Checks if law[start_index] marks the start of a structure.

    Args:
        structures: structure that we want to test against
        law: ordered list of strings that contain the text of the law we want to parse
        start_index: law[start_index] indicates the 1st line of the structure we want to check

    Returns:
        bool: True if law[start_index] marks the start of the structure argument passed in

    Examples:
        e.g
        >>> law = [
        ...     'BAB X',
        ...     'GUGATAN KE PENGADILAN',
        ...     'Pengajuan gugatan dilakukan...'
        ... ]

        >>> is_start_of_structure(Structure.BAB_NUMBER, law, 0)
        True

        >>> is_start_of_structure(Structure.UU_TITLE_TOPIC, law, 0)
        False
    """
    # LIST INDEXES
    if structure in LIST_INDEX_STRUCTURES:
        regex = LIST_INDEX_DEFINITIONS[structure]['regex']
        assert isinstance(regex, str)
        return is_heading(
            regex,
            law[start_index]
        )
    # UNDANG UNDANG
    elif structure == Structure.UNDANG_UNDANG:
        return is_start_of_undang_undang(law, start_index)
    # AGREEMENT
    elif structure == Structure.OPENING:
        return is_start_of_opening(law, start_index)
    elif structure == Structure.UU_TITLE:
        return is_start_of_uu_title(law, start_index)
    elif structure == Structure.UU_TITLE_YEAR_AND_NUMBER:
        return is_start_of_uu_title_year_and_number(law, start_index)
    elif structure == Structure.UU_TITLE_TOPIC:
        return is_start_of_uu_title_topic(law, start_index)
    elif structure == Structure.PREFACE:
        return is_start_of_preface(law, start_index)
    elif structure == Structure.CONSIDERATIONS:
        return is_start_of_considerations(law, start_index)
    elif structure == Structure.PRINCIPLES:
        return is_start_of_principles(law, start_index)
    elif structure == Structure.AGREEMENT:
        return is_start_of_agreement(law, start_index)
    # BAB
    elif structure == Structure.BAB:
        return is_start_of_bab(law, start_index)
    elif structure == Structure.BAB_NUMBER:
        return is_start_of_bab_number(law, start_index)
    elif structure == Structure.BAB_TITLE:
        return is_start_of_bab_title(law, start_index)
    # PASAL
    elif structure == Structure.PASAL:
        return is_start_of_pasal(law, start_index)
    elif structure == Structure.PASAL_NUMBER:
        return is_start_of_pasal_number(law, start_index)
    # BAGIAN
    elif structure == Structure.BAGIAN:
        return is_start_of_bagian(law, start_index)
    elif structure == Structure.BAGIAN_NUMBER:
        return is_start_of_bagian_number(law, start_index)
    elif structure == Structure.BAGIAN_TITLE:
        return is_start_of_bagian_title(law, start_index)
    # PARAGRAF
    elif structure == Structure.PARAGRAF:
        return is_start_of_paragraf(law, start_index)
    elif structure == Structure.PARAGRAF_NUMBER:
        return is_start_of_paragraf_number(law, start_index)
    elif structure == Structure.PARAGRAF_TITLE:
        return is_start_of_paragraf_title(law, start_index)
    # PERUBAHAN SECTION
    elif structure == Structure.PERUBAHAN_SECTION:
        return is_start_of_perubahan_section(law, start_index)
    elif structure == Structure.PERUBAHAN_PASAL:
        return is_start_of_perubahan_pasal(law, start_index)
    elif structure == Structure.PERUBAHAN_BAB:
        return is_start_of_perubahan_bab(law, start_index)
    elif structure == Structure.PERUBAHAN_BAGIAN:
        return is_start_of_perubahan_bagian(law, start_index)
    elif structure == Structure.PENJELASAN_PERUBAHAN_SECTION:
        return is_start_of_penjelasan_perubahan_section(law, start_index)
    elif structure == Structure.PENJELASAN_PERUBAHAN_PASAL:
        return is_start_of_penjelasan_perubahan_pasal(law, start_index)
    elif structure == Structure.PENJELASAN_PERUBAHAN_BAB:
        return is_start_of_penjelasan_perubahan_bab(law, start_index)
    elif structure == Structure.PENJELASAN_PERUBAHAN_BAGIAN:
        return is_start_of_penjelasan_perubahan_bagian(law, start_index)
    # LIST
    elif structure == Structure.LIST:
        return is_start_of_list(law, start_index)
    elif structure == Structure.LIST_ITEM:
        return is_start_of_list_item(law, start_index)
    elif structure == Structure.LIST_INDEX:
        return is_start_of_list_index(law, start_index)
    # CLOSING
    elif structure == Structure.CLOSING:
        return is_start_of_closing(law, start_index)
    elif structure == Structure.LEMBARAN_NUMBER:
        return is_start_of_lembaran_number(law, start_index)
    # PENJELASAN
    elif structure == Structure.PENJELASAN:
        return is_start_of_penjelasan(law, start_index)
    elif structure == Structure.PENJELASAN_TITLE:
        return is_start_of_penjelasan_title(law, start_index)
    elif structure == Structure.PENJELASAN_UMUM:
        return is_start_of_penjelasan_umum(law, start_index)
    elif structure == Structure.PENJELASAN_UMUM_TITLE:
        return is_start_of_penjelasan_umum_title(law, start_index)
    elif structure == Structure.PENJELASAN_PASAL_DEMI_PASAL:
        return is_start_of_penjelasan_pasal_demi_pasal(law, start_index)
    elif structure == Structure.PENJELASAN_PASAL_DEMI_PASAL_TITLE:
        return is_start_of_penjelasan_pasal_demi_pasal_title(law, start_index)
    elif structure == Structure.PENJELASAN_PASAL:
        return is_start_of_penjelasan_pasal(law, start_index)
    elif structure == Structure.PENJELASAN_LIST_ITEM:
        return is_start_of_penjelasan_list_index_str(law[start_index])
    elif structure == Structure.UNORDERED_LIST:
        return is_start_of_unordered_list(law, start_index)
    elif structure == Structure.UNORDERED_LIST_ITEM:
        return is_start_of_unordered_list_item(law, start_index)
    elif structure == Structure.UNORDERED_LIST_INDEX:
        return is_start_of_unordered_list_index(law, start_index)
    elif structure == Structure.FORMATTED_MATH_ROW:
        return is_start_of_formatted_math_row(law, start_index)
    # OTHERS
    elif structure == Structure.PLAINTEXT:
        return is_start_of_plaintext(law, start_index)
    else:
        function_name = '_'.join(structure.value.lower().split(' '))
        raise Exception('is_start_of_' + function_name +
                        ' function does not exist')


def is_start_of_any(structures: List[Structure], law: List[str], start_index: int) -> bool:
    """Checks if law[start_index] marks the start of any one of a list of structure enums

    Args:
        structures: list of structure enums that we want to test against
        law: ordered list of strings that contain the text of the law we want to parse
        start_index: law[start_index] indicates the 1st line of the structure we want to check

    Returns:
        bool: True if law[start_index] marks the start of any one of the enums in structures

    Examples:
        e.g
        >>> law = [
        ...     'UNDANG-UNDANG REPUBLIK INDONESIA',
        ...     'NOMOR 14 TAHUN 2008',
        ...     'TENTANG',
        ...     'KETERBUKAAN INFORMASI PUBLIK',
        ...     'DENGAN RAHMAT TUHAN YANG MAHA ESA',
        ...     'PRESIDEN REPUBLIK INDONESIA,',
        ... ]

        >>> is_start_of_any([Structure.UU_TITLE, Structure.LIST, Structure.BAB_TITLE], law, 0)
        True

        >>> is_start_of_any([Structure.LIST, Structure.BAB_TITLE], law, 0)
        False
    """
    for structure in structures:
        if is_start_of_structure(structure, law, start_index):
            return True
    return False


def is_start_of_undang_undang(law: List[str], start_index: int) -> bool:
    """Checks if law[start_index] marks the start of an UNDANG_UNDANG structure.
    An UNDANG_UNDANG structure always begin with an OPENING structure, so the first line
    of an OPENING structure always marks the start of an UNDANG_UNDANG structure.

    Args:
        law: ordered list of strings that contain the text of the law we want to parse
        start_index: law[start_index] indicates the 1st line of the structure we want to check

    Returns:
        bool: True if law[start_index] marks the start of a UNDANG_UNDANG structure; False otherwise

    Examples:
        e.g
        >>> law = [
        ...     'UNDANG-UNDANG REPUBLIK INDONESIA',
        ...     'NOMOR 14 TAHUN 2008',
        ...     'TENTANG',
        ...     'KETERBUKAAN INFORMASI PUBLIK',
        ...     'DENGAN RAHMAT TUHAN YANG MAHA ESA',
        ...     'PRESIDEN REPUBLIK INDONESIA,',
        ... ]

        >>> is_start_of_undang_undang(law, 0)
        True
    """
    return is_start_of_opening(law, start_index)


def is_start_of_opening(law: List[str], start_index: int) -> bool:
    """Checks if law[start_index] marks the start of an OPENING structure.
    The first line of an OPENING structure is always an UU_TITLE structure

    Args:
        law: ordered list of strings that contain the text of the law we want to parse
        start_index: law[start_index] indicates the 1st line of the structure we want to check

    Returns:
        bool: True if law[start_index] marks the start of a UU_TITLE structure; False otherwise

    Examples:
        e.g
        >>> law = [
        ...     'UNDANG-UNDANG REPUBLIK INDONESIA',
        ...     'NOMOR 14 TAHUN 2008',
        ...     'TENTANG',
        ...     'KETERBUKAAN INFORMASI PUBLIK',
        ...     'DENGAN RAHMAT TUHAN YANG MAHA ESA',
        ...     'PRESIDEN REPUBLIK INDONESIA,',
        ... ]

        >>> is_start_of_opening(law, 0)
        True
    """
    return is_start_of_uu_title(law, start_index)


def is_start_of_uu_title(law: List[str], start_index: int) -> bool:
    """Checks if law[start_index] marks the start of a UU_TITLE structure.

    Args:
        law: ordered list of strings that contain the text of the law we want to parse
        start_index: law[start_index] indicates the 1st line of the structure we want to check

    Returns:
        bool: True if law[start_index] marks the start of a UU_TITLE structure; False otherwise

    Examples:
        e.g
        >>> law = [
        ...     'UNDANG-UNDANG REPUBLIK INDONESIA',
        ...     'NOMOR 14 TAHUN 2008',
        ...     'TENTANG',
        ...     'KETERBUKAAN INFORMASI PUBLIK',
        ...     'DENGAN RAHMAT TUHAN YANG MAHA ESA',
        ...     'PRESIDEN REPUBLIK INDONESIA,',
        ... ]

        >>> is_start_of_uu_title(law, 0)
        True
    """
    return 'UNDANG-UNDANG REPUBLIK INDONESIA' in law[start_index]


def is_start_of_uu_title_year_and_number(law: List[str], start_index: int) -> bool:
    """Checks if law[start_index] marks the start of a UU_TITLE_YEAR_AND_NUMBER structure.

    Args:
        law: ordered list of strings that contain the text of the law we want to parse
        start_index: law[start_index] indicates the 1st line of the structure we want to check

    Returns:
        bool: True if law[start_index] marks the start of a UU_TITLE_YEAR_AND_NUMBER structure; False otherwise

    Examples:
        e.g
        >>> law = [
        ...     'UNDANG-UNDANG REPUBLIK INDONESIA',
        ...     'NOMOR 14 TAHUN 2008',
        ...     'TENTANG',
        ...     'KETERBUKAAN INFORMASI PUBLIK',
        ...     'DENGAN RAHMAT TUHAN YANG MAHA ESA',
        ...     'PRESIDEN REPUBLIK INDONESIA,',
        ... ]

        >>> is_start_of_uu_title_year_and_number(law, 1)
        True
    """
    return is_heading('NOMOR [0-9]+ TAHUN [0-9]{4}', law[start_index])


def is_start_of_uu_title_topic(law: List[str], start_index: int) -> bool:
    """Checks if law[start_index] marks the start of a UU_TITLE_TOPIC structure. 
    The line right after a UU_TITLE_TOPIC structure is always a PREFACE structure, and 
    the line 2 before a UU_TITLE_TOPIC structure is always a UU_TITLE_YEAR_AND_NUMBER structure.

    Args:
        law: ordered list of strings that contain the text of the law we want to parse
        start_index: law[start_index] indicates the 1st line of the structure we want to check

    Returns:
        bool: True if law[start_index] marks the start of a UU_TITLE_TOPIC structure; False otherwise

    Examples:
        e.g
        >>> law = [
        ...     'UNDANG-UNDANG REPUBLIK INDONESIA',
        ...     'NOMOR 14 TAHUN 2008',
        ...     'TENTANG',
        ...     'KETERBUKAAN INFORMASI PUBLIK',
        ...     'DENGAN RAHMAT TUHAN YANG MAHA ESA',
        ...     'PRESIDEN REPUBLIK INDONESIA,',
        ... ]

        >>> is_start_of_uu_title_topic(law, 3)
        True
    """
    return is_start_of_uu_title_year_and_number(law, start_index-2) and \
        is_start_of_preface(law, start_index+1)


def is_start_of_preface(law: List[str], start_index: int) -> bool:
    """Checks if law[start_index] marks the start of a PREFACE structure.

    Args:
        law: ordered list of strings that contain the text of the law we want to parse
        start_index: law[start_index] indicates the 1st line of the structure we want to check

    Returns:
        bool: True if law[start_index] marks the start of a PREFACE structure; False otherwise

    Examples:
        e.g
        >>> law = [
        ...     'DENGAN RAHMAT TUHAN YANG MAHA ESA',
        ...     'PRESIDEN REPUBLIK INDONESIA,',
        ...     'Menimbang:',
        ...     'a. bahwa keterbukaan...',
        ... ]

        >>> is_start_of_preface(law, 0)
        True
    """
    return 'DENGAN RAHMAT TUHAN YANG MAHA ESA' in law[start_index]


def is_start_of_considerations(law: List[str], start_index: int) -> bool:
    """Checks if law[start_index] marks the start of a CONSIDERATIONS structure.

    Args:
        law: ordered list of strings that contain the text of the law we want to parse
        start_index: law[start_index] indicates the 1st line of the structure we want to check

    Returns:
        bool: True if law[start_index] marks the start of a CONSIDERATIONS structure; False otherwise

    Examples:
        e.g
        >>> law = [
        ...     'Menimbang:', 
        ...     'a. bahwa informasi...', 
        ...     'b. bahwa hak...',
        ...     'c. bahwa keterbukaan...',
        ... ]

        >>> is_start_of_considerations(law, 0)
        True
    """
    return 'Menimbang:' in law[start_index]


def is_start_of_principles(law: List[str], start_index: int) -> bool:
    """Checks if law[start_index] marks the start of a PRINCIPLES structure.

    Args:
        law: ordered list of strings that contain the text of the law we want to parse
        start_index: law[start_index] indicates the 1st line of the structure we want to check

    Returns:
        bool: True if law[start_index] marks the start of a PRINCIPLES structure; False otherwise

    Examples:
        e.g
        >>> law = [
        ...     'Mengingat:',
        ...     'Pasal 20 Undang-Undang Dasar Negara Republik Indonesia Tahun 1945.',
        ... ]

        >>> is_start_of_principles(law, 0)
        True
    """
    return 'Mengingat:' in law[start_index]


def is_start_of_agreement(law: List[str], start_index: int) -> bool:
    """Checks if law[start_index] marks the start of a AGREEMENT structure.

    Args:
        law: ordered list of strings that contain the text of the law we want to parse
        start_index: law[start_index] indicates the 1st line of the structure we want to check

    Returns:
        bool: True if law[start_index] marks the start of a AGREEMENT structure; False otherwise

    Examples:
        e.g
        >>> law = [
        ...     'Dengan Persetujuan Bersama:',
        ...     'DEWAN PERWAKILAN RAKYAT REPUBLIK INDONESIA',
        ...     'dan',
        ...     'PRESIDEN REPUBLIK INDONESIA',
        ...     'MEMUTUSKAN:',
        ...     'Menetapkan:',
        ...     'UNDANG-UNDANG TENTANG KETERBUKAAN INFORMASI PUBLIK',
        ... ]

        >>> is_start_of_agreement(law, 0)
        True
    """
    return 'Dengan Persetujuan' in law[start_index] or \
        'Dengan persetujuan' == law[start_index]


def is_start_of_pasal(law: List[str], start_index: int, ) -> bool:
    """Checks if law[start_index] marks the start of a PASAL structure. The first line of a
    PASAL structure always begins with a PASAL_NUMBER structure.

    Args:
        law: ordered list of strings that contain the text of the law we want to parse
        start_index: law[start_index] indicates the 1st line of the structure we want to check

    Returns:
        bool: True if law[start_index] marks the start of a PASAL structure; False otherwise

    Examples:
        e.g
        >>> law = [
        ...     'Ketentuan lebih lanjut...',
        ...     'Pasal 12',
        ...     'Perizinan Berusaha',
        ... ]

        >>> is_start_of_pasal(law, 1)
        True
    """
    return is_start_of_pasal_number(law, start_index)


def is_start_of_pasal_number(law: List[str], start_index: int) -> bool:
    """Checks if law[start_index] marks the start of a PASAL_NUMBER structure.

    Args:
        law: ordered list of strings that contain the text of the law we want to parse
        start_index: law[start_index] indicates the 1st line of the structure we want to check

    Returns:
        bool: True if law[start_index] marks the start of a PASAL_NUMBER structure; False otherwise

    Examples:
        e.g
        >>> law = [
        ...     'BAB IV',
        ...     'Persyaratan Dasar',
        ...     'Pasal 18',
        ...     'Sesuai dengan...',
        ... ]

        >>> is_start_of_pasal_number(law, 2)
        True
    """
    return is_heading(PASAL_NUMBER_REGEX, law[start_index])


def is_start_of_perubahan_pasal(law: List[str], start_index: int) -> bool:
    return is_start_of_pasal(law, start_index) or \
        is_heading(PASAL_NUMBER_WITH_OPEN_QUOTE_CHAR_REGEX, law[start_index])


def is_start_of_penjelasan_perubahan_pasal(law: List[str], start_index: int) -> bool:
    return is_start_of_pasal(law, start_index) or \
        is_heading(PASAL_NUMBER_WITH_OPEN_QUOTE_CHAR_REGEX, law[start_index])


def is_start_of_penjelasan_pasal(law: List[str], start_index: int, ) -> bool:
    return is_start_of_pasal(law, start_index)


def is_start_of_perubahan_section(law: List[str], start_index: int) -> bool:
    '''
    TODO what if open/quote chars occur naturally in line
    '''
    line = law[start_index]
    return line[0] == OPEN_QUOTE_CHAR and CLOSE_QUOTE_CHAR not in line


def is_start_of_penjelasan_perubahan_section(law: List[str], start_index: int) -> bool:
    return is_start_of_perubahan_section(law, start_index)


def is_start_of_bagian(law: List[str], start_index: int) -> bool:
    """Checks if law[start_index] marks the start of a BAGIAN structure. The first line of a
    BAGIAN structure always begins with a BAGIAN_NUMBER structure.

    Args:
        law: ordered list of strings that contain the text of the law we want to parse
        start_index: law[start_index] indicates the 1st line of the structure we want to check

    Returns:
        bool: True if law[start_index] marks the start of a BAGIAN structure; False otherwise

    Examples:
        e.g
        >>> law = [
        ...     'Ketentuan lebih lanjut...',
        ...     'Bagian Ketujuh',
        ...     'Perizinan Berusaha',
        ...     'Pasal 5',
        ... ]

        >>> is_start_of_bagian(law, 1)
        True
    """
    return is_start_of_bagian_number(law, start_index)


def is_start_of_bagian_number(law: List[str], start_index: int) -> bool:
    """Checks if law[start_index] marks the start of a BAGIAN_NUMBER structure.

    Args:
        law: ordered list of strings that contain the text of the law we want to parse
        start_index: law[start_index] indicates the 1st line of the structure we want to check

    Returns:
        bool: True if law[start_index] marks the start of a BAGIAN_NUMBER structure; False otherwise

    Examples:
        e.g
        >>> law = [
        ...     'Dalam hal kegiatan...',
        ...     'Bagian Keempat',
        ...     'Izin Berusaha',
        ...     'Pasal 15',
        ... ]

        >>> is_start_of_bagian_number(law, 1)
        True
    """

    '''
    Bagian numbers are mostly in the format of 'kesatu', 'kedua', etc.
    however on rare occasions the 1st bagian can be 'pertama' instead
    of 'kesatu'
    '''
    return is_heading(BAGIAN_NUMBER_REGEX, law[start_index])


def is_start_of_bagian_title(law: List[str], start_index: int) -> bool:
    """Checks if law[start_index] marks the start of a BAGIAN_TITLE structure.
    The line right before a BAGIAN_TITLE structure is always a BAGIAN_NUMBER.

    Args:
        law: ordered list of strings that contain the text of the law we want to parse
        start_index: law[start_index] indicates the 1st line of the structure we want to check

    Returns:
        bool: True if law[start_index] marks the start of a BAGIAN_TITLE structure; False otherwise

    Examples:
        e.g
        >>> law = [
        ...     'Bagian Ketiga',
        ...     'Persyaratan Dasar',
        ...     'Pasal 18',
        ...     'Sesuai dengan...',
        ... ]

        >>> is_start_of_bagian_title(law, 1)
        True
    """
    return is_start_of_bagian_number(law, start_index-1)


def is_start_of_perubahan_bagian(law: List[str], start_index: int) -> bool:
    return is_start_of_bagian(law, start_index) or \
        is_heading(BAGIAN_NUMBER_WITH_OPEN_QUOTE_CHAR_REGEX, law[start_index])


def is_start_of_penjelasan_perubahan_bagian(law: List[str], start_index: int) -> bool:
    return is_start_of_bagian(law, start_index) or \
        is_heading(BAGIAN_NUMBER_WITH_OPEN_QUOTE_CHAR_REGEX, law[start_index])


def is_start_of_paragraf(law: List[str], start_index: int) -> bool:
    """Checks if law[start_index] marks the start of a PARAGRAF structure. The first line of a
    PARAGRAF structure always begins with a PARAGRAF_NUMBER structure.

    Args:
        law: ordered list of strings that contain the text of the law we want to parse
        start_index: law[start_index] indicates the 1st line of the structure we want to check

    Returns:
        bool: True if law[start_index] marks the start of a PARAGRAF structure; False otherwise

    Examples:
        e.g
        >>> law = [
        ...     'Ketentuan lebih lanjut...',
        ...     'Paragraf 2',
        ...     'Perizinan Berusaha',
        ...     'Pasal 5',
        ... ]

        >>> is_start_of_paragraf(law, 1)
        True
    """
    return is_start_of_paragraf_number(law, start_index)


def is_start_of_paragraf_number(law: List[str], start_index: int) -> bool:
    """Checks if law[start_index] marks the start of a PARAGRAF_NUMBER structure.

    Args:
        law: ordered list of strings that contain the text of the law we want to parse
        start_index: law[start_index] indicates the 1st line of the structure we want to check

    Returns:
        bool: True if law[start_index] marks the start of a PARAGRAF_NUMBER structure; False otherwise

    Examples:
        e.g
        >>> law = [
        ...     'Dalam hal kegiatan...',
        ...     'Paragraf 2',
        ...     'Izin Berusaha',
        ...     'Pasal 5',
        ... ]

        >>> is_start_of_paragraf_number(law, 1)
        True
    """
    return is_heading(PARAGRAF_NUMBER_REGEX, law[start_index])


def is_start_of_paragraf_title(law: List[str], start_index: int) -> bool:
    """Checks if law[start_index] marks the start of a PARAGRAF_TITLE structure.
    The line right before a PARAGRAF_TITLE structure is always a PARAGRAF_NUMBER.

    Args:
        law: ordered list of strings that contain the text of the law we want to parse
        start_index: law[start_index] indicates the 1st line of the structure we want to check

    Returns:
        bool: True if law[start_index] marks the start of a PARAGRAF_TITLE structure; False otherwise

    Examples:
        e.g
        >>> law = [
        ...     'Paragraf 2',
        ...     'Izin Berusaha',
        ...     'Pasal 5',
        ...     'Badan hukum yang...',
        ... ]

        >>> is_start_of_paragraf_title(law, 1)
        True
    """
    return is_start_of_paragraf_number(law, start_index-1)


def is_start_of_bab(law: List[str], start_index: int) -> bool:
    """Checks if law[start_index] marks the start of a BAB structure. The first line of a 
    BAB structure always begins with a BAB_NUMBER structure.

    Args:
        law: ordered list of strings that contain the text of the law we want to parse
        start_index: law[start_index] indicates the 1st line of the structure we want to check

    Returns:
        bool: True if law[start_index] marks the start of a BAB structure; False otherwise

    Examples:
        e.g
        >>> law = [
        ...     'Ketentuan lebih lanjut...',
        ...     'BAB XIV',
        ...     'KOMISI INFORMASI',
        ...     'Pasal 23',
        ... ]

        >>> is_start_of_bab(law, 1)
        True
    """
    return is_start_of_bab_number(law, start_index)


def is_start_of_bab_number(law: List[str], start_index: int) -> bool:
    """Checks if law[start_index] marks the start of a BAB_NUMBER structure.

    Args:
        law: ordered list of strings that contain the text of the law we want to parse
        start_index: law[start_index] indicates the 1st line of the structure we want to check

    Returns:
        bool: True if law[start_index] marks the start of a BAB_NUMBER structure; False otherwise

    Examples:
        e.g
        >>> law = [
        ...     'BAB XIV',
        ...     'KOMISI INFORMASI',
        ...     'Pasal 23',
        ... ]

        >>> is_start_of_bab_number(law, 0)
        True
    """
    return is_heading(BAB_NUMBER_REGEX, law[start_index])


def is_start_of_bab_title(law: List[str], start_index: int) -> bool:
    """Checks if law[start_index] marks the start of a BAB_TITLE structure.
    The line right before a BAB_TITLE structure is always a BAB_NUMBER.

    Args:
        law: ordered list of strings that contain the text of the law we want to parse
        start_index: law[start_index] indicates the 1st line of the structure we want to check

    Returns:
        bool: True if law[start_index] marks the start of a BAB_TITLE structure; False otherwise

    Examples:
        e.g
        >>> law = [
        ...     'Untuk mewujudkan...',
        ...     'BAB II',
        ...     'ASAS DAN TUJUAN',
        ...     'Pasal 1',
        ...     'Kewajiban...',
        ... ]

        >>> is_start_of_bab_title(law, 2)
        True
    """
    return is_start_of_bab_number(law, start_index-1)


def is_start_of_perubahan_bab(law: List[str], start_index: int) -> bool:
    return is_start_of_bab(law, start_index) or \
        is_heading(BAB_NUMBER_WITH_OPEN_QUOTE_CHAR_REGEX, law[start_index])


def is_start_of_penjelasan_perubahan_bab(law: List[str], start_index: int) -> bool:
    return is_start_of_bab(law, start_index) or \
        is_heading(BAB_NUMBER_WITH_OPEN_QUOTE_CHAR_REGEX, law[start_index])


def is_start_of_closing(law: List[str], start_index: int) -> bool:
    """Checks if law[start_index] marks the start of a CLOSING structure.

    Args:
        law: ordered list of strings that contain the text of the law we want to parse
        start_index: law[start_index] indicates the 1st line of the structure we want to check

    Returns:
        bool: True if law[start_index] marks the start of a CLOSING structure; False otherwise

    Examples:
        e.g
        >>> law = [
        ...     'Agar setiap orang mengetahuinya, memerintahkan pengundangan Undang-Undang ini dengan penempatannya dalam Lembaran Negara Republik Indonesia.'
        ...     'Disahkan Di Jakarta,',
        ...     'Pada Tanggal 25 Maret 2003',
        ...     'PRESIDEN REPUBLIK INDONESIA,',
        ...     'Ttd.',
        ...     'MEGAWATI SOEKARNOPUTRI',
        ...     'Diundangkan Di Jakarta,',
        ...     'Pada Tanggal 25 Maret 2003',
        ...     'SEKRETARIS NEGARA REPUBLIK INDONESIA',
        ...     'Ttd.',
        ...     'BAMBANG KESOWO',
        ...     'LEMBARAN NEGARA REPUBLIK INDONESIA TAHUN 2003 NOMOR 39 ',
        ...     ...,
        ... ]

        >>> is_start_of_closing(law, 1)
        True
    """
    return 'Lembaran Negara Republik Indonesia'.lower() in law[start_index-1].lower() and\
        (
            'Disahkan Di Jakarta'.lower() in law[start_index].lower() or
            'Diundangkan Di Jakarta'.lower() in law[start_index].lower() or
            'Ditetapkan Di Jakarta'.lower() in law[start_index].lower()
    )


def is_start_of_lembaran_number(law: List[str], start_index: int) -> bool:
    """Checks if law[start_index] marks the start of a LEMBARAN_NUMBER structure.

    Args:
        law: ordered list of strings that contain the text of the law we want to parse
        start_index: law[start_index] indicates the 1st line of the structure we want to check

    Returns:
        bool: True if law[start_index] marks the start of a LEMBARAN_NUMBER structure; False otherwise

    Examples:
        e.g
        >>> law = [
        ...     'LEMBARAN NEGARA REPUBLIK INDONESIA TAHUN 2003 NOMOR 39 ',
        ...     ...,
        ... ]

        >>> is_start_of_lembaran_number(law, 0)
        True
    """
    return is_heading(
        r'LEMBARAN NEGARA REPUBLIK INDONESIA TAHUN [0-9]{4} NOMOR [0-9]+',
        law[start_index]
    )


def is_start_of_penjelasan(law: List[str], start_index: int) -> bool:
    """Checks if law[start_index] marks the start of a PENJELASAN structure.
    A PENJELASAN structure always begin with a PENJELASAN_TITLE structure, and the first line
    of an PENJELASAN_TITLE structure always marks the start of an PENJELASAN structure.

    Args:
        law: ordered list of strings that contain the text of the law we want to parse
        start_index: law[start_index] indicates the 1st line of the structure we want to check

    Returns:
        bool: True if law[start_index] marks the start of a PENJELASAN structure; False otherwise

    Examples:
        e.g
        >>> law = [
        ...     'PENJELASAN',
        ...     'UNDANG-UNDANG REPUBLIK INDONESIA',
        ...     'NOMOR 13 TAHUN 2003',
        ...     'TENTANG',
        ...     'KETENAGAKERJAA',
        ... ]

        >>> is_start_of_penjelasan(law, 0)
        True
    """
    return is_start_of_penjelasan_title(law, start_index)


def is_start_of_penjelasan_umum(law: List[str], start_index: int) -> bool:
    return is_start_of_penjelasan_umum_title(law, start_index)


def is_start_of_penjelasan_umum_title(law: List[str], start_index: int) -> bool:
    return is_heading(r'(I\. )?UMUM', law[start_index]) or is_heading(r'PENJELASAN UMUM', law[start_index])


def is_start_of_penjelasan_title(law: List[str], start_index: int) -> bool:
    """Checks if law[start_index] marks the start of a PENJELASAN_TITLE structure.

    Args:
        law: ordered list of strings that contain the text of the law we want to parse
        start_index: law[start_index] indicates the 1st line of the structure we want to check

    Returns:
        bool: True if law[start_index] marks the start of a PENJELASAN_TITLE structure; False otherwise

    Examples:
        e.g
        >>> law = [
        ...     'PENJELASAN',
        ...     'UNDANG-UNDANG REPUBLIK INDONESIA',
        ...     'NOMOR 13 TAHUN 2003',
        ...     'TENTANG',
        ...     'KETENAGAKERJAA',
        ... ]

        >>> is_start_of_penjelasan_title(law, 0)
        True
    """
    heuristic_1 = is_heading(r'PENJELASAN', law[start_index]) and \
        is_heading(r'UNDANG-UNDANG REPUBLIK INDONESIA', law[start_index+1])

    heuristic_2 = is_heading(r'PENJELASAN', law[start_index]) and \
        is_heading(r'ATAS', law[start_index+1]) and \
        is_heading(r'UNDANG-UNDANG REPUBLIK INDONESIA', law[start_index+2])

    heuristic_3 = is_heading(r'PENJELASAN', law[start_index]) and \
        is_heading(
            r'RANCANGAN UNDANG-UNDANG REPUBLIK INDONESIA',
            law[start_index+1],
    )

    heuristic_4 = is_heading(r'PENJELASAN', law[start_index]) and \
        is_heading(r'ATAS', law[start_index+1]) and \
        is_heading(
            r'UNDANG-UNDANG NOMOR [0-9]+ TAHUN [0-9]{4}', law[start_index+2])

    return heuristic_1 or heuristic_2 or heuristic_3 or heuristic_4


def is_start_of_penjelasan_pasal_demi_pasal(law: List[str], start_index: int) -> bool:
    return is_start_of_penjelasan_pasal_demi_pasal_title(law, start_index)


def is_start_of_penjelasan_pasal_demi_pasal_title(law: List[str], start_index: int) -> bool:
    return is_heading(PENJELASAN_PASAL_DEMI_PASAL_REGEX, law[start_index])


def is_start_of_list(law: List[str], start_index: int) -> bool:
    """Checks if law[start_index] marks the start of a LIST structure.

    Args:
        law: ordered list of strings that contain the text of the law we want to parse
        start_index: law[start_index] indicates the 1st line of the structure we want to check

    Returns:
        bool: True if law[start_index] marks the start of a LIST structure; False otherwise

    Examples:
        e.g
        >>> law = [
        ...     'Pasal 4',
        ...     'Undang-Undang ini bertujuan untuk:',
        ...     'a.',
        ...     'menjamin hak warga negara...',
        ...     'b.',
        ...     'mendorong partisipasi...',
        ... ]

        >>> is_start_of_list(law, 1)
        False

        >>> is_start_of_list(law, 2)
        True

        >>> is_start_of_list(law, 4)
        False
    """
    return is_start_of_first_list_index(law[start_index])


def is_start_of_list_item(law: List[str], start_index: int) -> bool:
    """Checks if law[start_index] marks the start of a LIST_ITEM structure.

    Args:
        law: ordered list of strings that contain the text of the law we want to parse
        start_index: law[start_index] indicates the 1st line of the structure we want to check

    Returns:
        bool: True if law[start_index] marks the start of a LIST_ITEM structure; False otherwise

    Examples:
        e.g
        >>> law = [
        ...     'Undang-Undang ini bertujuan untuk:',    
        ...     'a.',
        ...     'menjamin hak warga negara...',
        ... ]

        >>> is_start_of_list_item(law, 0)
        False

        >>> is_start_of_list_item(law, 1)
        True

        >>> is_start_of_list_item(law, 2)
        False
    """
    return is_start_of_list_index(law, start_index)


def is_start_of_list_index(law: List[str], start_index: int) -> bool:
    """Checks if law[start_index] marks the start of a LIST_INDEX structure.

    Args:
        law: ordered list of strings that contain the text of the law we want to parse
        start_index: law[start_index] indicates the 1st line of the structure we want to check

    Returns:
        bool: True if law[start_index] marks the start of a LIST_INDEX structure; False otherwise

    Examples:
        e.g
        >>> law = [
        ...     'a.',
        ...     'dengan adanya...',
        ...     '1.',
        ...     'dengan adanya...',
        ...     '(1)',
        ...     'dengan adanya...',
        ... ]

        >>> is_start_of_list_index(law, 0)
        True

        >>> is_start_of_list_index(law, 1)
        False

        >>> is_start_of_list_index(law, 2)
        True

        >>> is_start_of_list_index(law, 4)
        True
    """
    return is_start_of_list_index_str(law[start_index])


def is_start_of_list_index_str(list_index_str: str) -> bool:
    """
    See is_start_of_list_index
    """
    for list_index_definition in LIST_INDEX_DEFINITIONS.values():
        regex = list_index_definition['regex']
        assert isinstance(regex, str)

        if is_heading(regex, list_index_str):
            return True

    return False


def is_start_of_penjelasan_list_index_str(list_index_str: str) -> bool:
    """
    See is_start_of_list_index
    """
    for list_index_definition in PENJELASAN_LIST_INDEX_DEFINITIONS.values():
        regex = list_index_definition['regex']
        assert isinstance(regex, str)

        if is_heading(regex, list_index_str):
            return True

    return False


def is_start_of_unordered_list(law: List[str], start_index: int) -> bool:
    return is_start_of_unordered_list_index(law, start_index)


def is_start_of_unordered_list_item(law: List[str], start_index: int) -> bool:
    return is_start_of_unordered_list_index(law, start_index)


def is_start_of_unordered_list_index(law: List[str], start_index: int) -> bool:
    maybe_list_index = law[start_index].split()[0].strip()
    return is_start_of_unordered_list_index_str(maybe_list_index)


def is_start_of_unordered_list_index_str(string: str) -> bool:
    # \u2212 is the minus sign
    return is_heading('\u2212', string) or is_heading('-', string)


def is_start_of_formatted_math_row(law: List[str], start_index: int) -> bool:
    line = law[start_index]

    match = re.search(FORMATTED_MATH_ROW_SPLIT_REGEX, line)
    if match is None:
        return False

    print_line()
    print(line)
    print_line()
    print('Is this line a FORMATTED_MATH_ROW?')

    pyperclip.copy(line)
    while True:
        print_yes_no()
        user_input = input()
        if user_input == 'y':
            return True
        elif user_input == 'n':
            return False
        else:
            print('Invalid input - try again!')


def is_start_of_plaintext(law: List[str], start_index: int) -> bool:
    # TODO: This is hilariously dumb. We should take in a list of the other
    # child structures as an argument and check against that instead
    # of literally every other structure
    all_other_structures = list(
        filter(lambda s: s != Structure.PLAINTEXT, list(Structure)))

    for structure in all_other_structures:
        if is_start_of_structure(structure, law, start_index):
            return False

    return True


def is_start_of_first_list_index(string: str) -> bool:
    """Check if string marks the start of a 'first' LIST_INDEX structure. 'First' in this 
    context refers to a LIST_INDEX structure that appears at the beginning of a LIST structure.
    See below for examples. In the future, we may need to also include alphanumeric strings e.g '1a.'

    Args:
        string: self-descriptive

    Returns:
        bool: True if string marks the start of a first LIST_INDEX structure; False otherwise

    Examples:
        >>> is_start_of_first_list_index('a.')
        True

        >>> is_start_of_first_list_index('b.')
        False

        >>> is_start_of_first_list_index('1.')
        True

        >>> is_start_of_first_list_index('2.')
        False

        >>> is_start_of_first_list_index('(1)')
        True

        >>> is_start_of_first_list_index('(2)')
        False

        >>> is_start_of_first_list_index('Ayat (1)')
        True

        >>> is_start_of_first_list_index('Huruf a')
        True

        >>> is_start_of_first_list_index('dengan adanya...')
        False
    """
    list_index = string.strip()
    return list_index in FIRST_LIST_INDEXES


def is_heading(regex: str, string: str) -> bool:
    """Checks if string matches the pattern regex with only whitespace on either side,
    which is the format that section headings in law PDFs often come in.

    If you're not familiar w/ regex (i.e regular expressions) see https://regexone.com/

    Args:
        regex: regex string the string will be checked against e.g 'BAB [0-9]+'
        string: string to be checked 

    Returns:
        bool: True if a heading, False otherwise

    Examples:
        >>> is_heading('BAB [0-9]+', ' BAB 23 ')
        True

        >>> is_heading('BAB [0-9]+', 'dengan BAB 23 ')
        False
    """
    return re.match(r'^[\s]*' + regex + r'[\s]*$', string) != None
