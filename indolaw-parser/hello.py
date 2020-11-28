import json
from enum import Enum
import sys
import re
from itertools import filterfalse


class ListType(Enum):
    INVALID = 0
    NUMBER_IN_BRACKETS = 1
    NUMBER_WITH_DOT = 2
    LETTER_WITH_DOT = 3


class Structure(Enum):
    # END = "End"
    # SKIP = "Skip"
    UNDANG_UNDANG = "Undang Undang"
    BAB = "Bab"
    BAB_NUMBER = "Bab Number"
    BAB_TITLE = "Bab Title"
    PASAL = "Pasal"
    PASAL_NUMBER = "Pasal Number"
    BAGIAN = "Bagian"
    BAGIAN_TITLE = "Bagian Title"
    BAGIAN_NUMBER = "Bagian Number"
    PARAGRAF = "Paragraf"
    PARAGRAF_TITLE = "Paragraf Title"
    PARAGRAF_NUMBER = "Paragraf Number"
    PLAINTEXT = "Plaintext"
    # LIST = "List"
    # LIST_ITEM = "List Item"
    # LIST_INDEX = "List Index"
    # NUMBER_IN_BRACKETS = "Number in Brackets"
    # NUMBER_WITH_DOT = "Number with Dot"
    # LETTER_WITH_DOT = "Letter with Dot"
# Structures that do not have child structures,
# and resolve to either a regex or just any unstructured text
PRIMITIVE_STRUCTURES = [
    Structure.PLAINTEXT,
    Structure.BAB_NUMBER,
    Structure.BAB_TITLE,
    Structure.PASAL_NUMBER,
    Structure.BAGIAN_NUMBER,
    Structure.BAGIAN_TITLE,
    Structure.PARAGRAF_NUMBER,
    Structure.PARAGRAF_TITLE
]


'''
-----------------

UTILS

-----------------
'''


def is_heading(regex, string):
    return re.match('^[\s]*' + regex + '[\s]*$', string) != None


def ignore_line(line):
    # end of page
    if ". . ." in line:
        return True
    # page number
    elif re.match('- [0-9]+ -', line.rstrip()) != None:
        return True
    else:
        return False


def detect_list_type(line):
    # e.g (5)
    # TODO(johnamadeo): Use regex instead - this doesn't work for (12)
    if line[0] == "(" and line[2] == ")":
        return ListType.NUMBER_IN_BRACKETS
    # e.g 5.
    # TODO(johnamadeo): Use regex instead - this doesn't work for 112.
    elif (line[1] == '.' or line[2] == '.') and line[0].isdigit():
        return ListType.NUMBER_WITH_DOT
    # e.g c.
    elif line[1] == '.' and line[0].islower():
        return ListType.LETTER_WITH_DOT
    else:
        return ListType.INVALID


'''
-----------------

IS_START_OF_X FUNCTIONS

TODO: If we add a HEADING_STRUCTURES & HEADING_TITLE_STRUCTURES enum,
we can reduce the number of is_heading calls to 1

-----------------
'''


def is_start_of_structure(structure, law, start_index):
    '''
    Assume that all the start of structure X heuristics are mutually exclusive
    i.e if one of the is_start_of_X functions returns True, all the other 
    is_start_of_X functions return False
    '''
    if structure == Structure.UNDANG_UNDANG:
        return is_start_of_undang_undang(law, start_index)
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
    # OTHERS
    elif structure == Structure.PLAINTEXT:
        return is_start_of_plaintext(law, start_index)
    else:
        function_name = '_'.join(structure.value.lower().split(' '))
        raise Exception('is_start_of_' + function_name +
                        ' function does not exist')


def is_start_of_undang_undang(law, start_index):
    return 'UNDANG-UNDANG' in law[start_index]


def is_start_of_pasal(law, start_index):
    return is_heading('Pasal[\s]+[0-9]+', law[start_index])


def is_start_of_pasal_number(law, start_index):
    return is_start_of_pasal(law, start_index)


def is_start_of_bagian(law, start_index):
    return is_heading('Bagian Ke[a-z]+', law[start_index])


def is_start_of_bagian_number(law, start_index):
    return is_start_of_bagian(law, start_index)


def is_start_of_bagian_title(law, start_index):
    return is_start_of_bagian_number(law, start_index-1)


def is_start_of_paragraf(law, start_index):
    return is_heading('Paragraf[\s]+[0-9]+', law[start_index])


def is_start_of_paragraf_number(law, start_index):
    return is_start_of_paragraf(law, start_index)


def is_start_of_paragraf_title(law, start_index):
    return is_start_of_paragraf_number(law, start_index-1)


def is_start_of_bab(law, start_index):
    return is_heading('BAB [MDCLXVI]+', law[start_index])


def is_start_of_bab_number(law, start_index):
    return is_start_of_bab(law, start_index)


def is_start_of_bab_title(law, start_index):
    return is_start_of_bab_number(law, start_index-1)


def is_start_of_plaintext(law, start_index):
    # TODO: This is hilariously dumb. We should take in a list of the other
    # child structures as an argument and check against that instead
    # of literally every other structure
    all_other_structures = list(
        filter(lambda s: s != Structure.PLAINTEXT, list(Structure)))

    for structure in all_other_structures:
        if is_start_of_structure(structure, law, start_index):
            return False

    return True


'''
-----------------

PARSE_X GENERIC FUNCTIONS

-----------------
'''


def parse_structure(structure, law, start_index):
    if structure in PRIMITIVE_STRUCTURES:
        return parse_primitive(structure, law, start_index)
    else:
        raise Exception("parse_" + structure.value +
                        " function does not exist")


def parse_primitive(structure, law, start_index, return_end_index=True):
    parsed_structure = {
        'type': structure.value,
        'text': law[start_index].rstrip()
    }

    if return_end_index:
        return parsed_structure, start_index
    else:
        return parsed_structure


def parse_complex_structure(
    law,
    start_index,
    # doesn't have to include root structure (i.e UNDANG_UNDANG)
    ancestor_structures,
    sibling_structures,
    child_structures
):
    '''
    This is the core algorithm for parsing a complex structure: a structure that is
    composed of other structures(a.k.a child structures).

    At a high level, the logic is:
    - let's say we know that structure X (e.g a Pasal) starts at line no. Y
    - starting from line line no.:
        - check if current line is the end of structure X 
        (e.g have we arrived at another Pasal? or is this the end of the Bab that the Pasal is in?)
        - if yes, return the hierarchy for structure X, along w/ the line no. at which structure X ends

        - check if current line is the start of a child structure
        - if yes, recursively call the parsing function that handles that child structure
        - the parsing function that handles the child structure will return:
            - the hierarchy for the child structure
            - the line no. Z at which the child structure ends

        - repeat the process starting at line no. Z+1
    - return hierarchy for structure X, along w/ the line no. W at which structure X ends

    If this doesn't feel intuitive, the best way to understand the algorithm is go through the text
    of the law by hand w/ pen and paper and apply the algorithm as implemented below!
    '''

    parsed_structure = []

    end_index = start_index-1
    while end_index < len(law)-1:
        structure = None

        # check if we've reached the end of this structure by checking
        # if this is the start of a sibling or ancestor structure
        for ancestor_or_sibling_structure in ancestor_structures + sibling_structures:
            if is_start_of_structure(ancestor_or_sibling_structure, law, start_index):
                return parsed_structure, end_index

        # check if we've reached the start of a child structure
        for child_structure in child_structures:
            if is_start_of_structure(child_structure, law, start_index):
                structure = child_structure
                break

        if structure == None:
            raise Exception(
                'Unable to detect the right structure for line: ' + law[start_index])

        parsed_sub_structure, end_index = parse_structure(
            structure, law, start_index)
        start_index = end_index + 1

        parsed_structure.append(parsed_sub_structure)

    return parsed_structure, end_index


    law = list(filterfalse(ignore_line, law))



if __name__ == "__main__":
    filename = "tes.txt"
    if len(sys.argv) > 2:
        filename = sys.argv[1]

    file = open(
        filename + '.txt',
        mode='r',
        encoding='utf-8-sig')
    law = file.read().split("\n")

    structured_law = parse_law(law)

    with open(filename + '.json', 'w') as outfile:
        json.dump(structured_law, outfile)

