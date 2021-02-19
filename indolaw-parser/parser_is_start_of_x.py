from typing import List
import re

from parser_types import Structure


def is_start_of_structure(structure: Structure, law: List[str], start_index: int) -> bool:
    '''
    Assume that all the start of structure X heuristics are mutually exclusive
    i.e if one of the is_start_of_X functions returns True, all the other
    is_start_of_X functions return False
    '''
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
    # OTHERS
    elif structure == Structure.PLAINTEXT:
        return is_start_of_plaintext(law, start_index)
    else:
        function_name = '_'.join(structure.value.lower().split(' '))
        raise Exception('is_start_of_' + function_name +
                        ' function does not exist')


def is_start_of_undang_undang(law: List[str], start_index: int) -> bool:
    return is_start_of_opening(law, start_index)


def is_start_of_opening(law: List[str], start_index: int) -> bool:
    return is_start_of_uu_title(law, start_index)


def is_start_of_uu_title(law: List[str], start_index: int) -> bool:
    return 'UNDANG-UNDANG REPUBLIK INDONESIA' in law[start_index]


def is_start_of_uu_title_year_and_number(law: List[str], start_index: int) -> bool:
    return is_heading('NOMOR [0-9]+ TAHUN [0-9]{4}', law[start_index])


def is_start_of_uu_title_topic(law: List[str], start_index: int) -> bool:
    return is_start_of_uu_title_year_and_number(law, start_index-2) and \
        is_start_of_preface(law, start_index+1)


def is_start_of_preface(law: List[str], start_index: int) -> bool:
    return 'DENGAN RAHMAT TUHAN YANG MAHA ESA' in law[start_index]


def is_start_of_considerations(law: List[str], start_index: int) -> bool:
    return 'Menimbang:' in law[start_index]


def is_start_of_principles(law: List[str], start_index: int) -> bool:
    return 'Mengingat:' in law[start_index]


def is_start_of_agreement(law: List[str], start_index: int) -> bool:
    return 'Dengan Persetujuan Bersama:' in law[start_index]


def is_start_of_pasal(law: List[str], start_index: int) -> bool:
    return is_heading('Pasal[\s]+[0-9]+', law[start_index])


def is_start_of_pasal_number(law: List[str], start_index: int) -> bool:
    return is_start_of_pasal(law, start_index)


def is_start_of_bagian(law: List[str], start_index: int) -> bool:
    return is_heading('Bagian Ke[a-z]+', law[start_index])


def is_start_of_bagian_number(law: List[str], start_index: int) -> bool:
    return is_start_of_bagian(law, start_index)


def is_start_of_bagian_title(law: List[str], start_index: int) -> bool:
    return is_start_of_bagian_number(law, start_index-1)


def is_start_of_paragraf(law: List[str], start_index: int) -> bool:
    return is_heading('Paragraf[\s]+[0-9]+', law[start_index])


def is_start_of_paragraf_number(law: List[str], start_index: int) -> bool:
    return is_start_of_paragraf(law, start_index)


def is_start_of_paragraf_title(law: List[str], start_index: int) -> bool:
    return is_start_of_paragraf_number(law, start_index-1)


def is_start_of_bab(law: List[str], start_index: int) -> bool:
    return is_heading('BAB [MDCLXVI]+', law[start_index])


def is_start_of_bab_number(law: List[str], start_index: int) -> bool:
    return is_start_of_bab(law, start_index)


def is_start_of_bab_title(law: List[str], start_index: int) -> bool:
    return is_start_of_bab_number(law, start_index-1)


def is_start_of_list(law: List[str], start_index: int) -> bool:
    return is_start_of_list_item(law, start_index)


def is_start_of_list_item(law: List[str], start_index: int) -> bool:
    return is_start_of_list_index(law, start_index)


def is_start_of_list_index(law: List[str], start_index: int) -> bool:
    return is_start_of_letter_with_dot(law, start_index) or \
        is_start_of_number_with_dot(law, start_index) or \
        is_start_of_number_with_brackets(law, start_index)


'''
This pattern below is kind of redundant and can probably be removed
down the line; for now it's necessary (ctrl+f the callsites to see why)
'''


def is_start_of_letter_with_dot(law: List[str], start_index: int) -> bool:
    line = law[start_index].split()[0]
    return is_start_of_letter_with_dot_str(line)


def is_start_of_letter_with_dot_str(string: str) -> bool:
    return is_heading('[a-z]\.', string)


def is_start_of_number_with_dot(law: List[str], start_index: int) -> bool:
    line = law[start_index].split()[0]
    return is_start_of_number_with_dot_str(line)


def is_start_of_number_with_dot_str(string: str) -> bool:
    return is_heading('[0-9]+\.', string)


def is_start_of_number_with_brackets(law: List[str], start_index: int) -> bool:
    line = law[start_index].split()[0]
    return is_start_of_number_with_brackets_str(line)


def is_start_of_number_with_brackets_str(string: str) -> bool:
    return is_heading('\([0-9]+\)', string)


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
    list_index = string.split()[0]
    return list_index in set(['a.', '1.', '(1)'])


def is_start_of_any(structures: List[Structure], law: List[str], start_index: int) -> bool:
    for structure in structures:
        if is_start_of_structure(structure, law, start_index):
            return True
    return False


def is_heading(regex: str, string: str) -> bool:
    return re.match('^[\s]*' + regex + '[\s]*$', string) != None
