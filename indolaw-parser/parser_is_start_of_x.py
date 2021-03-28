from typing import List
import re

from parser_types import Structure


def is_start_of_structure(structure: Structure, law: List[str], start_index: int) -> bool:
    """Checks if law[start_index] marks the start of a structure.

    We assume that all is_start_of_x heuristics are mutually exclusive
    i.e if one of the is_start_of_x functions returns True, all the other
    is_start_of_x functions return False

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
    if structure == Structure.UNDANG_UNDANG:
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
    # LIST
    elif structure == Structure.LIST:
        return is_start_of_list(law, start_index)
    elif structure == Structure.LIST_ITEM:
        return is_start_of_list_item(law, start_index)
    elif structure == Structure.LIST_INDEX:
        return is_start_of_list_index(law, start_index)
    elif structure == Structure.LETTER_WITH_DOT:
        return is_start_of_letter_with_dot(law, start_index)
    elif structure == Structure.NUMBER_WITH_DOT:
        return is_start_of_number_with_dot(law, start_index)
    elif structure == Structure.NUMBER_WITH_BRACKETS:
        return is_start_of_number_with_brackets(law, start_index)
    # CLOSING
    elif structure == Structure.CLOSING:
        return is_start_of_closing(law, start_index)
    elif structure == Structure.LEMBARAN_NUMBER:
        return is_start_of_lembaran_number(law, start_index)
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
    return 'Dengan Persetujuan Bersama' in law[start_index]


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
    return is_heading(r'Pasal[\s]+[0-9]+', law[start_index])


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
    return is_heading(r'Bagian Ke[a-z]+', law[start_index]) or \
        is_heading(r'Bagian Pertama', law[start_index])


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
    return is_heading(r'Paragraf[\s]+[0-9]+', law[start_index])


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
    return is_heading(r'BAB [MDCLXVI]+', law[start_index])


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


def is_start_of_closing(law: List[str], start_index: int) -> bool:
    return 'Lembaran Negara Republik Indonesia'.lower() in law[start_index-1].lower() and\
        'Disahkan Di Jakarta'.lower() in law[start_index].lower()


def is_start_of_lembaran_number(law: List[str], start_index: int) -> bool:
    return is_heading(
        r'LEMBARAN NEGARA REPUBLIK INDONESIA TAHUN [0-9]{4} NOMOR [0-9]+',
        law[start_index]
    )


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
    return is_start_of_letter_with_dot_str(list_index_str) or \
        is_start_of_number_with_dot_str(list_index_str) or \
        is_start_of_number_with_brackets_str(list_index_str)


'''
This pattern below is somewhat redundant and can probably be removed
down the line; for now it's necessary (ctrl+f the callsites to see why)
'''


def is_start_of_letter_with_dot(law: List[str], start_index: int) -> bool:
    """See documentation for is_start_of_letter_with_dot_str

    Args:
        law: ordered list of strings that contain the text of the law we want to parse
        start_index: law[start_index] indicates the 1st line of the structure we want to check

    Returns:
        bool: True if law[start_index] marks the start of a LETTER_WITH_DOT structure; False otherwise

    Examples:
        e.g
        >>> law = [
        ...     'a.',
        ...     'dengan adanya...',
        ...     'b.',
        ... ]

        >>> is_start_of_letter_with_dot(law, 0)
        True

        >>> is_start_of_letter_with_dot(law, 1)
        False

        >>> is_start_of_letter_with_dot(law, 2)
        True
    """
    line = law[start_index].split()[0]
    return is_start_of_letter_with_dot_str(line)


def is_start_of_letter_with_dot_str(string: str) -> bool:
    """Check if string marks the start of a LETTER_WITH_DOT structure.

    e.g consider this LIST structure
    >>> [
    ...     'a.' # LIST_INDEX
    ...     'dengan adanya cara baru...',
    ...     'b.' # LIST_INDEX
    ...     'yang dimaksud oleh...',
    ...     '(1)', # LIST_INDEX
    ...     'karena data...',
    ... ]

    'a.' and 'b.' marks the start of a LETTER_WITH_DOT, but not '(1)'

    Args:
        string: self-descriptive

    Returns:
        bool: True if string marks the start of a LETTER_WITH_DOT structure; False otherwise

    Examples:
        >>> is_start_of_letter_with_dot_str('a.')
        True

        >>> is_start_of_letter_with_dot_str('1.')
        False
    """
    return is_heading(r'[a-z]\.', string)


def is_start_of_number_with_dot(law: List[str], start_index: int) -> bool:
    """See documentation for is_start_of_number_with_dot_str

    Args:
        law: ordered list of strings that contain the text of the law we want to parse
        start_index: law[start_index] indicates the 1st line of the structure we want to check

    Returns:
        bool: True if law[start_index] marks the start of a NUMBER_WITH_DOT structure; False otherwise

    Examples:
        e.g
        >>> law = [
        ...     '1.',
        ...     'dengan adanya...',
        ...     '2.',
        ... ]

        >>> is_start_of_number_with_dot(law, 0)
        True

        >>> is_start_of_number_with_dot(law, 1)
        False

        >>> is_start_of_number_with_dot(law, 2)
        True
    """
    line = law[start_index].split()[0]
    return is_start_of_number_with_dot_str(line)


def is_start_of_number_with_dot_str(string: str) -> bool:
    """Check if string marks the start of a NUMBER_WITH_DOT structure.

    e.g consider this LIST structure
    >>> [
    ...     '1.' # LIST_INDEX
    ...     'dengan adanya cara baru...',
    ...     '2.' # LIST_INDEX
    ...     'yang dimaksud oleh...',
    ...     '(1)', # LIST_INDEX
    ...     'karena data...',
    ... ]

    '1.' and '2.' marks the start of a NUMBER_WITH_DOT, but not '(1)'

    Args:
        string: self-descriptive

    Returns:
        bool: True if string marks the start of a NUMBER_WITH_DOT structure; False otherwise

    Examples:
        >>> is_start_of_number_with_dot_str('2.')
        True

        >>> is_start_of_number_with_dot_str('b.')
        False
    """
    return is_heading(r'[0-9]+\.', string)


def is_start_of_number_with_brackets(law: List[str], start_index: int) -> bool:
    """See documentation for is_start_of_number_with_brackets_str

    Args:
        law: ordered list of strings that contain the text of the law we want to parse
        start_index: law[start_index] indicates the 1st line of the structure we want to check

    Returns:
        bool: True if law[start_index] marks the start of a NUMBER_WITH_BRACKETS structure; False otherwise

    Examples:
        e.g
        >>> law = [
        ...     '(1)',
        ...     'dengan adanya...',
        ...     '(2)',
        ... ]

        >>> is_start_of_number_with_brackets(law, 0)
        True

        >>> is_start_of_number_with_brackets(law, 1)
        False

        >>> is_start_of_number_with_brackets(law, 2)
        True
    """
    line = law[start_index].split()[0]
    return is_start_of_number_with_brackets_str(line)


def is_start_of_number_with_brackets_str(string: str) -> bool:
    """Check if string marks the start of a NUMBER_WITH_BRACKETS structure.

    e.g consider this LIST structure
    >>> [
    ...     '(1)' # LIST_INDEX
    ...     'dengan adanya cara baru...',
    ...     '(2)' # LIST_INDEX
    ...     'yang dimaksud oleh...', 
    ...     'a.', # LIST_INDEX
    ...     'karena data...',
    ... ]

    '(1)' and '(2)' marks the start of a NUMBER_WITH_BRACKETS, but not 'a.'

    Args:
        string: self-descriptive

    Returns:
        bool: True if string marks the start of a NUMBER_WITH_BRACKETS structure; False otherwise

    Examples:
        >>> is_start_of_number_with_brackets_str('(2)')
        True

        >>> is_start_of_number_with_brackets_str('b.')
        False
    """
    return is_heading(r'\([0-9]+\)', string)


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

    e.g consider this LIST structure
    >>> [
    ...    '1.' # LIST_INDEX
    ...    'dengan adanya cara baru...', # PLAINTEXT
    ...    '2.' # LIST_INDEX
    ...    'yang dimaksuh oleh...', # PLAINTEXT
    ... ]

    In the example above, '1.' is a first LIST_INDEX and '2.' is not, because
    only '1.' can appear at the beginning of a LIST.


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

        >>> is_start_of_first_list_index('dengan adanya...')
        False
    """
    list_index = string.split()[0]
    return list_index in set(['a.', '1.', '(1)'])


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
