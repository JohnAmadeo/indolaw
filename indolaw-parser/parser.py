import json
from enum import Enum
import sys
import re
from itertools import filterfalse


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
    LIST = "List"
    LIST_ITEM = "List Item"
    LIST_INDEX = "List Index"
    NUMBER_WITH_BRACKETS = "Number with Brackets"
    NUMBER_WITH_DOT = "Number with Dot"
    LETTER_WITH_DOT = "Letter with Dot"


TEXT_BLOCK_STRUCTURES = [Structure.PLAINTEXT, Structure.LIST]

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

LIST_INDEX_STRUCTURES = [Structure.NUMBER_WITH_BRACKETS,
                         Structure.NUMBER_WITH_DOT, Structure.LETTER_WITH_DOT]

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
        return Structure.NUMBER_IN_BRACKETS
    # e.g 5.
    # TODO(johnamadeo): Use regex instead - this doesn't work for 112.
    elif (line[1] == '.' or line[2] == '.') and line[0].isdigit():
        return Structure.NUMBER_WITH_DOT
    # e.g c.
    elif line[1] == '.' and line[0].islower():
        return Structure.LETTER_WITH_DOT
    else:
        return Structure.INVALID
def clean_law(law):
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


'''
-----------------

IS_START_OF_X FUNCTIONS

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


def is_start_of_list(law, start_index):
    return is_start_of_list_item(law, start_index)


def is_start_of_list_item(law, start_index):
    return is_start_of_list_index(law, start_index)


def is_start_of_list_index(law, start_index):
    return is_start_of_letter_with_dot(law, start_index) or \
        is_start_of_number_with_dot(law, start_index) or \
        is_start_of_number_with_brackets(law, start_index)


def is_start_of_letter_with_dot(law, start_index):
    string = law[start_index].split(' ')[0]
    return string.isalpha() and string == '.'


def is_start_of_number_with_dot(law, start_index):
    string = law[start_index].split(' ')[0]
    return is_heading('[0-9]+\.', string)


def is_start_of_number_with_brackets(law, start_index):
    string = law[start_index].split(' ')[0]
    return is_heading('\([0-9]+\)', string)


def detect_list_type(line):
    # e.g (5)
    # TODO(johnamadeo): Use regex instead - this doesn't work for (12)
    if line[0] == "(" and line[2] == ")":
        return Structure.NUMBER_IN_BRACKETS
    # e.g 5.
    # TODO(johnamadeo): Use regex instead - this doesn't work for 112.
    elif (line[1] == '.' or line[2] == '.') and line[0].isdigit():
        return Structure.NUMBER_WITH_DOT
    # e.g c.
    elif line[1] == '.' and line[0].islower():
        return Structure.LETTER_WITH_DOT
    else:
        return Structure.INVALID


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
    elif structure == Structure.BAB:
        return parse_bab(law, start_index)
    elif structure == Structure.PASAL:
        return parse_pasal(law, start_index)
    elif structure == Structure.BAGIAN:
        return parse_bagian(law, start_index)
    elif structure == Structure.PARAGRAF:
        return parse_paragraf(law, start_index)
    elif structure == Structure.LIST:
        return parse_list(law, start_index)
    elif structure == Structure.LIST_ITEM:
        return parse_list_item(law, start_index)
    elif structure == Structure.LIST_INDEX:
        return parse_list_index(law, start_index)
    else:
        raise Exception("parse_" + structure.value +
                        " function does not exist")


# Convenience wrapper for parse_primitive that doesn't return the end index
def simple_parse_primitive(structure, law, start_index):
    return parse_primitive(structure, law, start_index, return_end_index=False)


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
    NOTE: List-related structures should be parsed by parse_list_item

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
    initial_start_index = start_index

    end_index = start_index-1
    while end_index < len(law)-1:
        structure = None

        # check if we've reached the end of this structure by checking
        # if this is the start of a sibling or ancestor structure
        for ancestor_or_sibling_structure in ancestor_structures + sibling_structures:
            if is_start_of_structure(ancestor_or_sibling_structure, law, start_index):
                return parsed_structure, end_index
        '''
        For a complex structure, the very 1st line must be part of
        the structure / cannot be the start of an ancestor or sibling
        structure.

        e.g if we are in parse_bab, the first time we see "BAB III" marks the
        start of the current bab, not the start of a sibling bab
        '''
        if start_index > initial_start_index:
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
        '''
        TODO(johnamadeo) See if more elegant way to handle list index
        '''
        if type(parsed_sub_structure) == dict and \
                'type' in parsed_sub_structure and \
                parsed_sub_structure['type'] == Structure.LIST_INDEX:
            start_index = end_index
        else:
            start_index = end_index + 1
        start_index = end_index + 1

        parsed_structure.append(parsed_sub_structure)

    return parsed_structure, end_index


'''
-----------------

PARSE_X FUNCTIONS

-----------------
'''


def parse_undang_undang(law):
    law = list(filterfalse(ignore_line, law))
    law = clean_law(law)
    return parse_complex_structure(
        law,
        0,
        ancestor_structures=[],
        sibling_structures=[],
        child_structures=[Structure.BAB],
    )


def parse_bab(law, start_index):
    parsed_structure = [
        simple_parse_primitive(Structure.BAB_NUMBER, law, start_index),
        simple_parse_primitive(Structure.BAB_TITLE, law, start_index+1),
    ]

    parsed_sub_structure, end_index = parse_complex_structure(
        law,
        start_index+2,
        ancestor_structures=[],
        sibling_structures=[Structure.BAB],
        child_structures=[Structure.PASAL, Structure.BAGIAN])
    parsed_structure.extend(parsed_sub_structure)

    return parsed_structure, end_index


def parse_pasal(law, start_index):
    parsed_structure = [
        simple_parse_primitive(Structure.PASAL_NUMBER, law, start_index),
    ]

    parsed_sub_structure, end_index = parse_complex_structure(
        law,
        start_index+1,
        ancestor_structures=[Structure.BAB,
                             Structure.BAGIAN, Structure.PARAGRAF],
        sibling_structures=[Structure.PASAL],
        child_structures=TEXT_BLOCK_STRUCTURES)
    parsed_structure.extend(parsed_sub_structure)

    return parsed_structure, end_index


def parse_bagian(law, start_index):
    parsed_structure = [
        simple_parse_primitive(Structure.BAGIAN_NUMBER, law, start_index),
        simple_parse_primitive(Structure.BAGIAN_TITLE, law, start_index+1),
    ]

    parsed_sub_structure, end_index = parse_complex_structure(
        law,
        start_index+2,
        ancestor_structures=[Structure.BAB],
        sibling_structures=[Structure.BAGIAN],
        child_structures=[Structure.PASAL, Structure.PARAGRAF])
    parsed_structure.extend(parsed_sub_structure)

    return parsed_structure, end_index


def parse_paragraf(law, start_index):
    parsed_structure = [
        simple_parse_primitive(Structure.PARAGRAF_NUMBER, law, start_index),
        simple_parse_primitive(Structure.PARAGRAF_TITLE, law, start_index+1),
    ]

    parsed_sub_structure, end_index = parse_complex_structure(
        law,
        start_index+2,
        ancestor_structures=[Structure.BAB, Structure.BAGIAN],
        sibling_structures=[Structure.PARAGRAF],
        child_structures=[Structure.PASAL])
    parsed_structure.extend(parsed_sub_structure)

    return parsed_structure, end_index


def parse_list(law, start_index):
    return parse_complex_structure(
        law,
        start_index,
        ancestor_structures=[Structure.PASAL,
                             Structure.PARAGRAF, Structure.BAGIAN, Structure.BAB],
        sibling_structures=[Structure.PLAINTEXT],
        child_structures=[Structure.LIST_ITEM])


def parse_list_item(law, start_index):
    return parse_complex_structure(
        law,
        start_index,
        # ancestor_structures=[Structure.PASAL, Structure.PARAGRAF,
        #                      Structure.BAGIAN, Structure.BAB, Structure.LIST],
        ancestor_structures=[Structure.PASAL, Structure.PARAGRAF,
                             Structure.BAGIAN, Structure.BAB],
        sibling_structures=[Structure.LIST_ITEM],
        child_structures=[Structure.LIST_INDEX] + TEXT_BLOCK_STRUCTURES)


def parse_list_index(law, start_index):
    if is_start_of_letter_with_dot(law, start_index):
        return parse_primitive(Structure.LETTER_WITH_DOT, law, start_index)
    elif is_start_of_number_with_dot(law, start_index):
        return parse_primitive(Structure.NUMBER_WITH_DOT, law, start_index),
    elif is_start_of_number_with_brackets(law, start_index):
        return parse_primitive(Structure.NUMBER_WITH_BRACKETS, law, start_index)


def parse_list_item_TEST(
    law,
    start_index,
    list_index,
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

        for ancestor_structure in ancestor_structures:
            # BUT WHAT IF THE ANCESTOR IS A LIST (i.e nested list)
            # nested list always have different type than
            # the direct ancestor
            if is_start_of_structure(ancestor_structure, law, start_index):
                return parsed_structure, end_index

            # if line is plaintext, it's a plaintext sibling and return

            # if line is a list item, compare the line no. and type against
            # the current line no. and type
            # if it's the same, keep going
            # if it's current + 1 (and same type), then we've reached a sibling
            # list item

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
        '''
        TODO(johnamadeo) See if more elegant way to handle list index
        '''
        if type(parsed_sub_structure) == dict and \
                'type' in parsed_sub_structure and \
                parsed_sub_structure['type'] == Structure.LIST_INDEX:
            start_index = end_index
        else:
            start_index = end_index + 1

        parsed_structure.append(parsed_sub_structure)

    return parsed_structure, end_index


'''
-----------------

__MAIN__

-----------------
'''

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('e.g python3 parser.py omnibus_law_m1')
        exit()

    filename = sys.argv[1]
    file = open(
        filename + '.txt',
        mode='r',
        encoding='utf-8-sig')
    law = file.read().split("\n")

    parsed_undang_undang, _ = parse_undang_undang(law)

    with open(filename + '.json', 'w') as outfile:
        json.dump(parsed_undang_undang, outfile)

'''
parse_undang_undang
    parse_bab
        parse_bab_number
        parse_bab_title
        parse_pasal
            parse_pasal_number
            parse_plaintext
            parse_list
'''
