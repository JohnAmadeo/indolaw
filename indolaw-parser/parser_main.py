import json
import sys
from typing import List, Tuple, Union

from parser_types import (
    Structure,
    Primitive,
    Complex,
    TEXT_BLOCK_STRUCTURES,
    PRIMITIVE_STRUCTURES,
)
from parser_is_start_of_x import (
    is_start_of_structure,
    is_start_of_first_list_index,
    is_start_of_any,
    is_start_of_plaintext,
    is_start_of_list,
    is_start_of_list_item,
    is_start_of_letter_with_dot,
    is_start_of_number_with_dot,
    is_start_of_number_with_brackets,
)
from parser_utils import (
    roman_to_int,
    node,
    get_list_index_type,
    is_next_list_index_number,
    clean_law,
    print_debug
)

'''
-----------------

PARSE_X GENERIC FUNCTIONS

-----------------
'''


def parse_structure(
    structure: Structure,
    law: List[str],
    start_index: int
) -> Tuple[Union[Primitive, Complex], int]:
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
def simple_parse_primitive(structure: Structure, law: List[str], start_index: int) -> Primitive:
    """Convenience wrapper for parse_primitive that doesn't return the end index. 
    See parse_primitive for more.
    """
    parsed_primitive, _ = parse_primitive(structure, law, start_index)
    return parsed_primitive


def parse_primitive(
    structure: Structure,
    law: List[str],
    start_index: int,
) -> Tuple[Primitive, int]:
    """Create a primitive structure. See the type definition of the Primitive structure for more. 

    Args:
        structure: the structure enum we want to assign to the primitive structure created
        law: ordered list of strings that contain the text of the law we want to parse
        start_index: law[start_index] is the text of the primitive structure created

    Returns:
        Primitive: the initial list of strings after transformations have been applied to it
        int: just start_index; 

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
    return Primitive(
        type=structure.value,
        text=law[start_index].rstrip()
    ), start_index


def parse_complex_structure(
    law: List[str],
    start_index: int,
    # doesn't have to include root structure (i.e UNDANG_UNDANG)
    ancestor_structures: List[Structure],
    sibling_structures: List[Structure],
    child_structures: List[Structure],
) -> Tuple[List[Union[Primitive, Complex]], int]:
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

    children_list: List[Union[Primitive, Complex]] = []
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
                    return children_list, end_index

        child_structure = None

        # check if we've reached the start of a child structure
        for maybe_child_structure in child_structures:
            if is_start_of_structure(maybe_child_structure, law, start_index):
                child_structure = maybe_child_structure
                break

        if child_structure == None:
            print_debug(law, start_index)
            raise Exception(
                f'''Unable to detect the right structure for line: {law[start_index]}''')

        assert child_structure is not None  # mypy type hint
        parsed_sub_structure, end_index = parse_structure(
            child_structure, law, start_index)
        start_index = end_index + 1

        children_list.append(parsed_sub_structure)

    return children_list, end_index


'''
-----------------

PARSE_X FUNCTIONS

-----------------
'''


def parse_undang_undang(law: List[str]) -> Tuple[Complex, int]:
    law = clean_law(law)

    # for l in law:
    #     print(l)
    # exit()

    parsed_opening, end_index = parse_opening(law, 0)
    parsed_children_list, _ = parse_complex_structure(
        law,
        end_index+1,
        ancestor_structures=[],
        sibling_structures=[],
        child_structures=[Structure.BAB],
    )

    return node(
        Structure.UNDANG_UNDANG,
        [
            parsed_opening,
            *parsed_children_list,
        ],
    ), end_index


def parse_opening(law: List[str], start_index: int) -> Tuple[Complex, int]:

    parsed_uu_title, end_index = parse_uu_title(law, start_index)
    parsed_preface, end_index = parse_preface(law, end_index+1)
    parsed_considerations, end_index = parse_considerations(law, end_index+1)
    parsed_principles, end_index = parse_principles(law, end_index+1)
    parsed_agreement, end_index = parse_agreement(law, end_index+1)

    return node(
        Structure.OPENING,
        [
            parsed_uu_title,
            parsed_preface,
            parsed_considerations,
            parsed_principles,
            parsed_agreement,
        ]
    ), end_index


def parse_uu_title(law: List[str], start_index: int) -> Tuple[Complex, int]:
    '''
    e.g 
    UNDANG-UNDANG REPUBLIK INDONESIA 
    NOMOR 14 TAHUN 2008 
    TENTANG 
    KETERBUKAAN INFORMASI PUBLIK 
    '''
    return node(
        Structure.UU_TITLE,
        [
            simple_parse_primitive(Structure.PLAINTEXT, law, start_index),
            simple_parse_primitive(
                Structure.UU_TITLE_YEAR_AND_NUMBER, law, start_index+1),
            simple_parse_primitive(
                Structure.PLAINTEXT, law, start_index+2),
            simple_parse_primitive(
                Structure.UU_TITLE_TOPIC, law, start_index+3),
        ],
    ), start_index+3


def parse_preface(law: List[str], start_index: int) -> Tuple[Complex, int]:
    return node(
        Structure.PREFACE,
        [
            simple_parse_primitive(Structure.PLAINTEXT, law, start_index),
            simple_parse_primitive(
                Structure.PLAINTEXT, law, start_index+1),
        ],
    ), start_index+1


def parse_considerations(law: List[str], start_index: int) -> Tuple[Complex, int]:
    parsed_primitive = simple_parse_primitive(
        Structure.PLAINTEXT, law, start_index)

    parsed_children_list, end_index = parse_complex_structure(
        law,
        start_index+1,
        # TODO(johnamadeo): clarify this; we don't REALLY need to enumerate all ancestors, only ancestors that might come AFTER
        ancestor_structures=[],
        # TODO(johnamadeo): rename to "next_sibling_structures"?
        sibling_structures=[Structure.PRINCIPLES],
        child_structures=TEXT_BLOCK_STRUCTURES,
    )

    return node(
        Structure.CONSIDERATIONS,
        [parsed_primitive, *parsed_children_list],
    ), end_index


def parse_principles(law: List[str], start_index: int) -> Tuple[Complex, int]:

    parsed_primitive = simple_parse_primitive(
        Structure.PLAINTEXT, law, start_index)
    parsed_children_list, end_index = parse_complex_structure(
        law,
        start_index+1,
        ancestor_structures=[],
        sibling_structures=[Structure.AGREEMENT],
        child_structures=TEXT_BLOCK_STRUCTURES,
    )
    return node(
        Structure.PRINCIPLES,
        [parsed_primitive, *parsed_children_list],
    ), end_index


def parse_agreement(law: List[str], start_index: int) -> Tuple[Complex, int]:
    '''
    e.g 
    Dengan Persetujuan Bersama: 
    DEWAN PERWAKILAN RAKYAT REPUBLIK INDONESIA 
    dan 
    PRESIDEN REPUBLIK INDONESIA 
    MEMUTUSKAN: 
    Menetapkan: 
    UNDANG-UNDANG TENTANG KETERBUKAAN INFORMASI PUBLIK 
    '''

    # this part is always 7 lines long
    return node(
        Structure.AGREEMENT,
        [simple_parse_primitive(
            Structure.PLAINTEXT, law, start_index+i) for i in range(7)]
    ), start_index+6


def parse_bab(law: List[str], start_index: int) -> Tuple[Complex, int]:
    parsed_bab_number = simple_parse_primitive(
        Structure.BAB_NUMBER, law, start_index)
    parsed_bab_title = simple_parse_primitive(
        Structure.BAB_TITLE, law, start_index+1)

    parsed_children_list, end_index = parse_complex_structure(
        law,
        start_index+2,
        ancestor_structures=[],
        sibling_structures=[Structure.BAB],
        child_structures=[Structure.PASAL, Structure.BAGIAN])

    # get bab number e.g "Bab IV" -> 4
    bab_number_roman = parsed_bab_number['text'].split()[1]
    bab_number_int = roman_to_int(bab_number_roman)

    return node(
        Structure.BAB,
        [
            parsed_bab_number,
            parsed_bab_title,
            *parsed_children_list,
        ],
        'bab-' + str(bab_number_int),
    ), end_index


def parse_pasal(law: List[str], start_index: int) -> Tuple[Complex, int]:
    parsed_pasal_number = simple_parse_primitive(
        Structure.PASAL_NUMBER, law, start_index)
    parsed_children_list, end_index = parse_complex_structure(
        law,
        start_index+1,
        ancestor_structures=[Structure.BAB,
                             Structure.BAGIAN, Structure.PARAGRAF],
        sibling_structures=[Structure.PASAL],
        child_structures=TEXT_BLOCK_STRUCTURES)

    return node(
        Structure.PASAL,
        [
            parsed_pasal_number,
            *parsed_children_list,
        ],
        'pasal-'+parsed_pasal_number['text'].split()[1],
    ), end_index


def parse_bagian(law: List[str], start_index: int) -> Tuple[Complex, int]:
    parsed_children_list, end_index = parse_complex_structure(
        law,
        start_index+2,
        ancestor_structures=[Structure.BAB],
        sibling_structures=[Structure.BAGIAN],
        child_structures=[Structure.PASAL, Structure.PARAGRAF])

    return node(
        Structure.BAGIAN,
        [
            simple_parse_primitive(Structure.BAGIAN_NUMBER, law, start_index),
            simple_parse_primitive(Structure.BAGIAN_TITLE, law, start_index+1),
            *parsed_children_list,
        ]
    ), end_index


def parse_paragraf(law: List[str], start_index: int) -> Tuple[Complex, int]:
    parsed_children_list, end_index = parse_complex_structure(
        law,
        start_index+2,
        ancestor_structures=[Structure.BAB, Structure.BAGIAN],
        sibling_structures=[Structure.PARAGRAF],
        child_structures=[Structure.PASAL])

    return node(
        Structure.PARAGRAF,
        [
            simple_parse_primitive(
                Structure.PARAGRAF_NUMBER, law, start_index),
            simple_parse_primitive(
                Structure.PARAGRAF_TITLE, law, start_index+1),
            *parsed_children_list,
        ]
    ), end_index


'''
in parse_list, we might run into ancestor lists, but not child lists, because 
any child lists should be embedded inside a list item
'''


def parse_list(law: List[str], start_index: int) -> Tuple[Complex, int]:
    structure = Structure.LIST
    children_list: List[Union[Primitive, Complex]] = []

    non_recursive_ancestors = [Structure.PASAL, Structure.PARAGRAF,
                               Structure.BAGIAN, Structure.BAB]

    initial_start_index = start_index
    end_index = start_index-1
    while end_index < len(law)-1:

        not_first_line = start_index > initial_start_index
        start_of_non_recursive_ancestors = is_start_of_any(
            non_recursive_ancestors, law, start_index)
        if not_first_line and start_of_non_recursive_ancestors:
            return node(structure, children_list), end_index

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
        if len(children_list) > 0:
            parsed_list_item = children_list[-1]
            '''
            known mypy problem: parsed_list_item is type Union[Primitive | Complex]
            but we know a list's children are all list items so parsed_list_item
            has to be type Complex
            '''
            parsed_list_index = parsed_list_item['children'][0]  # type: ignore
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
                return node(structure, children_list), end_index
            '''
            Suppose the current list is of type X (e.g NUMBER_WITH_DOT) and the current line
            is the start of a list item that is also of type X.

            If the current list item's number is NOT 1 larger than the last list item's number, then the 
            current list item can't be part of this list.

            i.e if the last list item's number is 10. and the current list item's number is 12. 
            or 5., the current list item is clearly not part of this list
            
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
                return node(structure, children_list), end_index
            else:
                # TODO(johnamadeo): Ask the human for input in this case
                pass

        # LIST's only child structure is LIST_ITEM
        parsed_list_item, end_index = parse_list_item(law, start_index)

        children_list.append(parsed_list_item)
        start_index = end_index + 1

    return node(structure, children_list), end_index


def parse_list_item(law: List[str], start_index: int) -> Tuple[Complex, int]:
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
    children_list = [
        parsed_list_index,
        parsed_plaintext,
    ]

    '''
    the 3rd line is either a nested list that is the child of this list item,
    or it marks the start of a sibling or ancestor structure
    '''
    non_recursive_ancestors = [Structure.PASAL, Structure.PARAGRAF,
                               Structure.BAGIAN, Structure.BAB,
                               Structure.PRINCIPLES, Structure.AGREEMENT]

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
            return node(structure, children_list), end_index

        child_structure = None
        # TODO(johnamadeo): see pg 17 Omnibus Law for embedded pasal problem
        if is_start_of_plaintext(law, start_index):
            child_structure = Structure.PLAINTEXT
        elif is_start_of_list_item(law, start_index):
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
                return node(structure, children_list), end_index

        if child_structure == None:
            raise Exception(
                'parse_list_item: child is neither a list or plaintext')

        assert child_structure is not None  # mypy type hint
        parsed_structure, end_index = parse_structure(
            child_structure, law, start_index)
        children_list.append(parsed_structure)
        start_index = end_index + 1

    return node(structure, children_list), end_index


def parse_list_index(law, start_index) -> Tuple[Primitive, int]:
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
