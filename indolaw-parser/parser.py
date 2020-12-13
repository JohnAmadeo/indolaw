import json
from enum import Enum
import sys
import re
from itertools import filterfalse


class Structure(Enum):
    # END = "End"
    # SKIP = "Skip"
    UNDANG_UNDANG = "UNDANG_UNDANG"
    BAB = "BAB"
    BAB_NUMBER = "BAB_NUMBER"
    BAB_TITLE = "BAB_TITLE"
    PASAL = "PASAL"
    PASAL_NUMBER = "PASAL_NUMBER"
    BAGIAN = "BAGIAN"
    BAGIAN_TITLE = "BAGIAN_TITLE"
    BAGIAN_NUMBER = "BAGIAN_NUMBER"
    PARAGRAF = "PARAGRAF"
    PARAGRAF_TITLE = "PARAGRAF_TITLE"
    PARAGRAF_NUMBER = "PARAGRAF_NUMBER"
    PLAINTEXT = "PLAINTEXT"
    LIST = "LIST"
    LIST_ITEM = "LIST_ITEM"
    LIST_INDEX = "LIST_INDEX"
    NUMBER_WITH_BRACKETS = "NUMBER_WITH_BRACKETS"
    NUMBER_WITH_DOT = "NUMBER_WITH_DOT"
    LETTER_WITH_DOT = "LETTER_WITH_DOT"


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


# https://www.w3resource.com/python-exercises/class-exercises/python-class-exercise-2.php
def roman_to_int(number):
    roman_values = {'I': 1, 'V': 5, 'X': 10,
                    'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    integer = 0
    for i in range(len(number)):
        if i > 0 and roman_values[number[i]] > roman_values[number[i - 1]]:
            integer += roman_values[number[i]] - \
                2 * roman_values[number[i - 1]]
        else:
            integer += roman_values[number[i]]
    return integer


def node(structure, children, id=''):
    # TODO(johnamadeo): This is just a placeholder for what should eventually become a proper Class constructor
    return {
        'type': structure.value,
        # this is to create a unique ID that can be used for HTML links
        'id': id,
        'children': children,
    }


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


def get_list_index_type(string):
    if type(string) is not str:
        return None

    if is_start_of_number_with_brackets_str(string):
        return Structure.NUMBER_WITH_BRACKETS
    elif is_start_of_number_with_dot_str(string):
        return Structure.NUMBER_WITH_DOT
    elif is_start_of_letter_with_dot_str(string):
        return Structure.LETTER_WITH_DOT
    else:
        return None


def get_list_index_as_num(regex, string):
    number_string = re.match(regex, string).group(1)
    # e.g '100'
    if number_string.isnumeric():
        return int(number_string)
    # e.g 'a'
    else:
        return ord(number_string)


def is_next_list_index_number(a, b):
    a_type = get_list_index_type(a)
    b_type = get_list_index_type(b)

    if b_type not in set(LIST_INDEX_STRUCTURES):
        raise Exception('next_list_index_number: Invalid input')
    if not (a_type == None or a_type == b_type):
        raise Exception('next_list_index_number: Invalid input')

    if a_type == None:
        return is_start_of_first_list_index(b)

    regex = None
    if a_type == Structure.NUMBER_WITH_BRACKETS:
        regex = '\(([0-9]+)\)'
    elif a_type == Structure.NUMBER_WITH_DOT:
        regex = '([0-9]+)\.'
    elif a_type == Structure.LETTER_WITH_DOT:
        regex = '([a-z])\.'

    return get_list_index_as_num(regex, a) + 1 == get_list_index_as_num(regex, b)


def is_start_of_first_list_index(string):
    list_index = string.split()[0]
    return list_index in set(['a.', '1.', '(1)'])


def is_start_of_any(structures, law, start_index):
    for structure in structures:
        if is_start_of_structure(structure, law, start_index):
            return True
    return False


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


'''
This pattern below is kind of redundant and can probably be removed
down the line; for now it's necessary (ctrl+f the callsites to see why)
'''


def is_start_of_letter_with_dot(law, start_index):
    line = law[start_index].split()[0]
    return is_start_of_letter_with_dot_str(line)


def is_start_of_letter_with_dot_str(string):
    return is_heading('[a-z]\.', string)


def is_start_of_number_with_dot(law, start_index):
    line = law[start_index].split()[0]
    return is_start_of_number_with_dot_str(line)


def is_start_of_number_with_dot_str(string):
    return is_heading('[0-9]+\.', string)


def is_start_of_number_with_brackets(law, start_index):
    line = law[start_index].split()[0]
    return is_start_of_number_with_brackets_str(line)


def is_start_of_number_with_brackets_str(string):
    return is_heading('\([0-9]+\)', string)


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
    structure,
    law,
    start_index,
    # doesn't have to include root structure (i.e UNDANG_UNDANG)
    ancestor_structures,
    sibling_structures,
    child_structures
):
    '''
    NOTE: List-related structures should be parsed by parse_list and parse_list_item

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

    children = []
    initial_start_index = start_index

    end_index = start_index-1
    while end_index < len(law)-1:
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
                    return node(structure, children), end_index

        child_structure = None

        # check if we've reached the start of a child structure
        for maybe_child_structure in child_structures:
            if is_start_of_structure(maybe_child_structure, law, start_index):
                child_structure = maybe_child_structure
                break

        if child_structure == None:
            raise Exception(
                'Unable to detect the right structure for line: ' + law[start_index])

        parsed_sub_structure, end_index = parse_structure(
            child_structure, law, start_index)
        start_index = end_index + 1

        children.append(parsed_sub_structure)

    return node(structure, children), end_index


'''
-----------------

PARSE_X FUNCTIONS

-----------------
'''


def parse_undang_undang(law):
    law = clean_law(law)

    # for l in law:
    #     print(l)
    # exit()

    return parse_complex_structure(
        Structure.UNDANG_UNDANG,
        law,
        0,
        ancestor_structures=[],
        sibling_structures=[],
        child_structures=[Structure.BAB],
    )


def parse_bab(law, start_index):
    children = [
        simple_parse_primitive(Structure.BAB_NUMBER, law, start_index),
        simple_parse_primitive(Structure.BAB_TITLE, law, start_index+1),
    ]

    parsed_sub_structure, end_index = parse_complex_structure(
        Structure.BAB,
        law,
        start_index+2,
        ancestor_structures=[],
        sibling_structures=[Structure.BAB],
        child_structures=[Structure.PASAL, Structure.BAGIAN])
    children.extend(parsed_sub_structure['children'])

    bab_number_roman = children[0]['text'].split()[1]
    bab_number_int = roman_to_int(bab_number_roman)

    return node(
        Structure.BAB,
        children,
        'bab-' + str(bab_number_int),
    ), end_index


def parse_pasal(law, start_index):
    children = [
        simple_parse_primitive(Structure.PASAL_NUMBER, law, start_index),
    ]

    parsed_sub_structure, end_index = parse_complex_structure(
        Structure.PASAL,
        law,
        start_index+1,
        ancestor_structures=[Structure.BAB,
                             Structure.BAGIAN, Structure.PARAGRAF],
        sibling_structures=[Structure.PASAL],
        child_structures=TEXT_BLOCK_STRUCTURES)
    children.extend(parsed_sub_structure['children'])

    return node(
        Structure.PASAL,
        children,
        'pasal-'+children[0]['text'].split()[1],
    ), end_index


def parse_bagian(law, start_index):
    children = [
        simple_parse_primitive(Structure.BAGIAN_NUMBER, law, start_index),
        simple_parse_primitive(Structure.BAGIAN_TITLE, law, start_index+1),
    ]

    parsed_sub_structure, end_index = parse_complex_structure(
        Structure.BAGIAN,
        law,
        start_index+2,
        ancestor_structures=[Structure.BAB],
        sibling_structures=[Structure.BAGIAN],
        child_structures=[Structure.PASAL, Structure.PARAGRAF])
    children.extend(parsed_sub_structure['children'])

    return node(Structure.BAGIAN, children), end_index


def parse_paragraf(law, start_index):
    children = [
        simple_parse_primitive(Structure.PARAGRAF_NUMBER, law, start_index),
        simple_parse_primitive(Structure.PARAGRAF_TITLE, law, start_index+1),
    ]

    parsed_sub_structure, end_index = parse_complex_structure(
        Structure.PARAGRAF,
        law,
        start_index+2,
        ancestor_structures=[Structure.BAB, Structure.BAGIAN],
        sibling_structures=[Structure.PARAGRAF],
        child_structures=[Structure.PASAL])
    children.extend(parsed_sub_structure['children'])

    return node(Structure.PARAGRAF, children), end_index


'''
in parse_list, we might run into ancestor lists, but not child lists, because 
any child lists should be embedded inside a list item
'''


def parse_list(law, start_index):
    structure = Structure.LIST
    children = []

    non_recursive_ancestors = [Structure.PASAL, Structure.PARAGRAF,
                               Structure.BAGIAN, Structure.BAB]

    initial_start_index = start_index
    end_index = start_index-1
    while end_index < len(law)-1:

        not_first_line = start_index > initial_start_index
        start_of_non_recursive_ancestors = is_start_of_any(
            non_recursive_ancestors, law, start_index)
        if not_first_line and start_of_non_recursive_ancestors:
            return node(structure, children), end_index

        '''
        If there is already 1 list item parsed, we need to check if the next list item
        is part of the same list or part of an ancestor list. 

        We know the next list item can't be part of a child list because if it was, 
        it would have been parsed by a parse_list_item call further down the recursion tree

        (this isn't super obvious and requires some thinking: try it on the e.g below)
        e.g
        1. 
        Hello world
            1.
            The quick brown fox
            2.
            The quick brown fox
        2.
        Hello world
        '''
        if len(children) > 0:
            parsed_list_item = children[-1]
            parsed_list_index = parsed_list_item['children'][0]
            curr_list_index_type = Structure[parsed_list_index['type']]
            curr_list_index_number = parsed_list_index['text']

            next_list_index_type = get_list_index_type(law[start_index])
            next_list_index_number = law[start_index].rstrip()
            '''
            Suppose the current list is of type NUMBER_WITH_DOT. But the current line
            is the start of a NUMBER_WITH_BRACKETS. 

            Therefore the list item that starts at this line cannot be part of this list
            (it can't be a child either - see comment block above this one). Hence, it 
            must be an ancestor
            '''
            if curr_list_index_type != next_list_index_type:
                return node(structure, children), end_index
            '''
            Suppose the current list is of type X (e.g NUMBER_WITH_DOT) and the current line
            is the start of a list item that is also of type X.

            If the current list item's number is NOT 1 larger than the last list item's number, then the 
            current list item can't be part of this list.

            i.e if the last list item's number is 10. and the current list item's number is 12. 
            or 5., the current list item is clearly not part of this list

            TODO(johnamadeo): Need to handle alphanumeric progression 24a. -> 24b.
            
            However, if the current list item's number is 1 larger than the last list item's number 
            (i.e a. -> b. OR (7) -> (8) OR 10. -> 11.) THERE IS NO 100% WAY to distinguish whether 
            this list item is part of the current list or an ancestor list

            This is because these 2 lists are indistinguishable:

            1. Lorem ipsum
            2. Lorem ipsum
                1. Lorem ipsum
                2. Lorem ipsum
                3. Lorem ipsum

            versus

            1. Lorem ipsum
            2. Lorem ipsum
                1. Lorem ipsum
                2. Lorem ipsum
            3. Lorem ipsum

            Suppose we are in the nested list, and we see "3. Lorem ipsum". We have
            no idea if "3. Lorem ipsum" is part of this list or an ancestor list 
            because they are equally valid.

            Heuristically, however, it's more likely that this current
            list item is indeed part of this list so that's what we assume for now.
            '''
            if not is_next_list_index_number(curr_list_index_number, next_list_index_number):
                return node(structure, children), end_index
            else:
                # TODO(johnamadeo): Ask the human for input in this case
                pass

        # LIST's only child structure is LIST_ITEM
        parsed_list_item, end_index = parse_list_item(law, start_index)
        children.append(parsed_list_item)
        start_index = end_index + 1

    return node(structure, children), end_index


def parse_list_item(law, start_index):
    '''
    The 1st and 2nd line of a list item must be a list index and plaintext.
    Even in the case of a nested list, there is always a plaintext in between
    the list index and the nested list

    e.g
    1.
    Ketentuan Undang Undang 23 diubah sebagai berikut:
        1. 
        Pasal 5 dihapus
        2. 
        Pasal 6 dihapus
    '''
    structure = Structure.LIST_ITEM
    parsed_list_index, _ = parse_structure(
        Structure.LIST_INDEX, law, start_index)
    parsed_plaintext = simple_parse_primitive(
        Structure.PLAINTEXT, law, start_index+1)
    children = [
        parsed_list_index,
        parsed_plaintext,
    ]

    '''
    From the 3rd line onwards, the child will either be a plaintext or a nested list
    '''
    non_recursive_ancestors = [Structure.PASAL, Structure.PARAGRAF,
                               Structure.BAGIAN, Structure.BAB]

    start_index += 2
    end_index = start_index-1
    while end_index < len(law)-1:
        '''
        Check if we're no longer in the list item and in an ancestor

        e.g
        Pasal 4
            1. 
            Abc
            2. 
            Abc
        Pasal 5

        If we're parsing the 2nd list item and we reach "Pasal 5", stop 
        parsing the list item and return up the recursion tree
        '''
        start_of_non_recursive_ancestors = is_start_of_any(
            non_recursive_ancestors, law, start_index)
        if start_of_non_recursive_ancestors:
            return node(structure, children), end_index

        '''
        A LIST ITEM's child can be a PLAINTEXT or a nested LIST
        '''
        child_structure = None
        if is_start_of_plaintext(law, start_index):
            child_structure = Structure.PLAINTEXT
        elif is_start_of_list(law, start_index):
            '''
            Need to decide if the list is a sibling, ancestor or child list. 

            If the list is a child list, we need to recursively parse the nested child list.
            If the list is a sibling or ancestor, stop parsing the list item and 
            return up the recursion tree

            Heuristics:
            1) Child -> list index number 1 (i.e if start of list)
            2) Sibling or Ancestor -> if not child

            Child e.g
            1. 
            abc
            2.
            abc
                1. abc
            '''
            next_list_index_number = law[start_index].rstrip()
            if is_start_of_first_list_index(next_list_index_number):
                child_structure = Structure.LIST
            else:
                return node(structure, children), end_index

        if child_structure == None:
            raise Exception(
                'parse_list_item: child is neither a list or plaintext')

        parsed_structure, end_index = parse_structure(
            child_structure, law, start_index)
        children.append(parsed_structure)
        start_index = end_index + 1

    return node(structure, children), end_index


def parse_list_index(law, start_index):
    if is_start_of_letter_with_dot(law, start_index):
        return parse_primitive(Structure.LETTER_WITH_DOT, law, start_index)
    elif is_start_of_number_with_dot(law, start_index):
        return parse_primitive(Structure.NUMBER_WITH_DOT, law, start_index)
    elif is_start_of_number_with_brackets(law, start_index):
        return parse_primitive(Structure.NUMBER_WITH_BRACKETS, law, start_index)
    else:
        raise Exception(
            "Unrecognized list index for line: " + law[start_index])


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
        json.dump(parsed_undang_undang, outfile, indent=2)
