import json
import sys
from typing import Any, Dict, List, Tuple, Union

from parser_types import (
    Structure,
    TEXT_BLOCK_STRUCTURES,
    PRIMITIVE_STRUCTURES,
    PrimitiveNode,
    ComplexNode
)
from parser_is_start_of_x import (
    is_start_of_structure,
    is_start_of_first_list_index,
    is_start_of_any,
    is_start_of_plaintext,
    is_start_of_list_item,
    is_start_of_letter_with_dot,
    is_start_of_number_with_dot,
    is_start_of_number_with_brackets,
)
from parser_utils import (
    convert_tree_to_json,
    get_list_index_type,
    is_next_list_index_number,
    clean_law,
    print_around
)

ROOT: Union[ComplexNode, None] = None

'''
-----------------

PARSE_X GENERIC FUNCTIONS

-----------------
'''


def parse_structure(
    parent: ComplexNode,
    structure: Structure,
    law: List[str],
    start_index: int
) -> int:
    if structure in PRIMITIVE_STRUCTURES:
        parent.add_child(PrimitiveNode(type=structure, text=law[start_index]))
        end_index = start_index
        return end_index

    elif structure == Structure.BAB:
        return parse_bab(parent, law, start_index)
    elif structure == Structure.PASAL:
        return parse_pasal(parent, law, start_index)
    elif structure == Structure.BAGIAN:
        return parse_bagian(parent, law, start_index)
    elif structure == Structure.PARAGRAF:
        return parse_paragraf(parent, law, start_index)
    elif structure == Structure.LIST:
        return parse_list(parent, law, start_index)
    elif structure == Structure.LIST_ITEM:
        return parse_list_item(parent, law, start_index)
    elif structure == Structure.LIST_INDEX:
        return parse_list_index(parent, law, start_index)
    else:
        crash(law, start_index, f'No function to parse {structure.value}')
        return -1  # only to satisfy mypy; will never run since we crash


def parse_complex_structure(
    parent: ComplexNode,
    law: List[str],
    start_index: int,
    # doesn't have to include root structure (i.e UNDANG_UNDANG)
    ancestor_structures: List[Structure],
    sibling_structures: List[Structure],
    child_structures: List[Structure],
) -> int:
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
                    return end_index

        child_structure = None

        # check if we've reached the start of a child structure
        for maybe_child_structure in child_structures:
            if is_start_of_structure(maybe_child_structure, law, start_index):
                child_structure = maybe_child_structure
                break

        if child_structure == None:
            crash(law, start_index,
                  f'Cannot find structure for line {start_index}')

        assert child_structure is not None  # mypy type hint
        end_index = parse_structure(parent, child_structure, law, start_index)
        start_index = end_index + 1

    return end_index


'''
-----------------

PARSE_X FUNCTIONS

-----------------
'''


def parse_undang_undang(law: List[str]):
    law = clean_law(law)

    # for l in law:
    #     print(l)
    # exit()

    global ROOT
    ROOT = ComplexNode(type=Structure.UNDANG_UNDANG)
    end_index = parse_opening(ROOT, law, 0)

    _ = parse_complex_structure(
        ROOT,
        law,
        end_index+1,
        ancestor_structures=[],
        sibling_structures=[],
        child_structures=[Structure.BAB],
    )


def parse_opening(parent: ComplexNode, law: List[str], start_index: int) -> int:
    opening_node = ComplexNode(type=Structure.OPENING)
    parent.add_child(opening_node)

    end_index = parse_uu_title(opening_node, law, start_index)
    end_index = parse_preface(opening_node, law, end_index+1)
    end_index = parse_considerations(opening_node, law, end_index+1)
    end_index = parse_principles(opening_node, law, end_index+1)
    end_index = parse_agreement(opening_node, law, end_index+1)

    return end_index


def parse_uu_title(parent: ComplexNode, law: List[str], start_index: int) -> int:
    '''
    e.g
    UNDANG-UNDANG REPUBLIK INDONESIA
    NOMOR 14 TAHUN 2008
    TENTANG
    KETERBUKAAN INFORMASI PUBLIK
    '''
    uu_title_node = ComplexNode(type=Structure.UU_TITLE)
    parent.add_child(uu_title_node)

    uu_title_node.add_child(PrimitiveNode(
        type=Structure.PLAINTEXT, text=law[start_index]))
    uu_title_node.add_child(PrimitiveNode(type=Structure.UU_TITLE_YEAR_AND_NUMBER,
                                          text=law[start_index+1]))
    uu_title_node.add_child(PrimitiveNode(
        type=Structure.PLAINTEXT, text=law[start_index+2]))
    uu_title_node.add_child(PrimitiveNode(type=Structure.UU_TITLE_TOPIC,
                                          text=law[start_index+3]))

    end_index = start_index+3
    return end_index


def parse_preface(parent: ComplexNode, law: List[str], start_index: int) -> int:
    preface_node = ComplexNode(type=Structure.PREFACE)
    parent.add_child(preface_node)

    preface_node.add_child(PrimitiveNode(
        type=Structure.PLAINTEXT, text=law[start_index]))
    preface_node.add_child(PrimitiveNode(
        type=Structure.PLAINTEXT, text=law[start_index+1]))

    end_index = start_index+1
    return end_index


def parse_considerations(parent: ComplexNode, law: List[str], start_index: int) -> int:
    considerations_node = ComplexNode(type=Structure.CONSIDERATIONS)
    parent.add_child(considerations_node)

    considerations_node.add_child(PrimitiveNode(
        type=Structure.PLAINTEXT, text=law[start_index]))

    end_index = parse_complex_structure(
        considerations_node,
        law,
        start_index+1,
        # TODO(johnamadeo): clarify this; we don't REALLY need to enumerate all ancestors, only ancestors that might come AFTER
        ancestor_structures=[],
        # TODO(johnamadeo): rename to "next_sibling_structures"?
        sibling_structures=[Structure.PRINCIPLES],
        child_structures=TEXT_BLOCK_STRUCTURES,
    )

    return end_index


def parse_principles(parent: ComplexNode, law: List[str], start_index: int) -> int:
    principles_node = ComplexNode(type=Structure.PRINCIPLES)
    parent.add_child(principles_node)

    principles_node.add_child(PrimitiveNode(
        type=Structure.PLAINTEXT, text=law[start_index]))

    end_index = parse_complex_structure(
        principles_node,
        law,
        start_index+1,
        ancestor_structures=[],
        sibling_structures=[Structure.AGREEMENT],
        child_structures=TEXT_BLOCK_STRUCTURES,
    )
    return end_index


def parse_agreement(parent: ComplexNode, law: List[str], start_index: int) -> int:
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
    agreement_node = ComplexNode(type=Structure.AGREEMENT)
    parent.add_child(agreement_node)

    for i in range(7):
        agreement_node.add_child(PrimitiveNode(
            type=Structure.PLAINTEXT, text=law[start_index+i]))

    # this part is always 7 lines long
    end_index = start_index+6
    return end_index


def parse_bab(parent: ComplexNode, law: List[str], start_index: int) -> int:
    bab_node = ComplexNode(type=Structure.BAB)
    parent.add_child(bab_node)

    bab_node.add_child(PrimitiveNode(
        type=Structure.BAB_NUMBER, text=law[start_index]))
    bab_node.add_child(PrimitiveNode(
        type=Structure.BAB_TITLE, text=law[start_index+1]))

    end_index = parse_complex_structure(
        bab_node,
        law,
        start_index+2,
        ancestor_structures=[],
        sibling_structures=[Structure.BAB],
        child_structures=[Structure.PASAL, Structure.BAGIAN])

    return end_index


def parse_pasal(parent: ComplexNode, law: List[str], start_index: int) -> int:
    pasal_node = ComplexNode(type=Structure.PASAL)
    parent.add_child(pasal_node)

    pasal_node.add_child(PrimitiveNode(
        type=Structure.PASAL_NUMBER, text=law[start_index]))

    end_index = parse_complex_structure(
        pasal_node,
        law,
        start_index+1,
        ancestor_structures=[Structure.BAB,
                             Structure.BAGIAN, Structure.PARAGRAF],
        sibling_structures=[Structure.PASAL],
        child_structures=TEXT_BLOCK_STRUCTURES)

    return end_index


def parse_bagian(parent: ComplexNode, law: List[str], start_index: int) -> int:
    bagian_node = ComplexNode(type=Structure.BAGIAN)
    parent.add_child(bagian_node)

    bagian_node.add_child(PrimitiveNode(
        type=Structure.BAGIAN_NUMBER, text=law[start_index]))
    bagian_node.add_child(PrimitiveNode(
        type=Structure.BAGIAN_TITLE, text=law[start_index+1]))

    end_index = parse_complex_structure(
        bagian_node,
        law,
        start_index+2,
        ancestor_structures=[Structure.BAB],
        sibling_structures=[Structure.BAGIAN],
        child_structures=[Structure.PASAL, Structure.PARAGRAF])

    return end_index


def parse_paragraf(parent: ComplexNode, law: List[str], start_index: int) -> int:
    paragraf_node = ComplexNode(type=Structure.PARAGRAF)
    parent.add_child(paragraf_node)

    paragraf_node.add_child(PrimitiveNode(
        type=Structure.PARAGRAF_NUMBER, text=law[start_index]))
    paragraf_node.add_child(PrimitiveNode(
        type=Structure.PARAGRAF_TITLE, text=law[start_index+1]))

    end_index = parse_complex_structure(
        paragraf_node,
        law,
        start_index+2,
        ancestor_structures=[Structure.BAB, Structure.BAGIAN],
        sibling_structures=[Structure.PARAGRAF],
        child_structures=[Structure.PASAL])

    return end_index


'''
in parse_list, we might run into ancestor lists, but not child lists, because
any child lists should be embedded inside a list item
'''


def parse_list(parent: ComplexNode, law: List[str], start_index: int) -> int:
    list_node = ComplexNode(type=Structure.LIST)
    parent.add_child(list_node)

    non_recursive_ancestors = [Structure.PASAL, Structure.PARAGRAF,
                               Structure.BAGIAN, Structure.BAB]

    initial_start_index = start_index
    end_index = start_index-1
    while end_index < len(law)-1:

        not_first_line = start_index > initial_start_index
        start_of_non_recursive_ancestors = is_start_of_any(
            non_recursive_ancestors, law, start_index)
        if not_first_line and start_of_non_recursive_ancestors:
            return end_index

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
        if len(list_node.children) > 0:
            list_item_node = list_node.children[-1]
            '''
            known mypy problem: parsed_list_item is type Union[Primitive | Complex]
            but we know a list's children are all list items so parsed_list_item
            has to be type Complex
            '''
            list_index_node = list_item_node.children[0]  # type: ignore
            assert isinstance(list_index_node, PrimitiveNode)
            curr_list_index_type = Structure[list_index_node.type.value]
            curr_list_index_number = list_index_node.text

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
                return end_index
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
                return end_index
            else:
                # TODO(johnamadeo): Ask the human for input in this case
                pass

        # LIST's only child structure is LIST_ITEM
        end_index = parse_list_item(list_node, law, start_index)
        start_index = end_index + 1

    return end_index


def parse_list_item(parent: ComplexNode, law: List[str], start_index: int) -> int:
    list_item_node = ComplexNode(type=Structure.LIST_ITEM)
    parent.add_child(list_item_node)

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
    _ = parse_list_index(list_item_node, law, start_index)
    list_item_node.add_child(PrimitiveNode(
        type=Structure.PLAINTEXT, text=law[start_index+1]))

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
            return end_index

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
                return end_index

        if child_structure == None:
            raise Exception(
                'parse_list_item: child is neither a list or plaintext')

        assert child_structure is not None  # mypy type hint
        end_index = parse_structure(
            list_item_node, child_structure, law, start_index)
        start_index = end_index + 1

    return end_index


def parse_list_index(parent: ComplexNode, law: List[str], start_index: int) -> int:
    end_index = start_index
    if is_start_of_letter_with_dot(law, start_index):
        parent.add_child(PrimitiveNode(
            type=Structure.LETTER_WITH_DOT, text=law[start_index]))
    elif is_start_of_number_with_dot(law, start_index):
        parent.add_child(PrimitiveNode(
            type=Structure.NUMBER_WITH_DOT, text=law[start_index]))
    elif is_start_of_number_with_brackets(law, start_index):
        parent.add_child(PrimitiveNode(
            type=Structure.NUMBER_WITH_BRACKETS, text=law[start_index]))
    else:
        crash(law, start_index, f'line {start_index} is not a list index')

    return end_index


'''
-----------------

__MAIN__

-----------------
'''


def read(filename):
    file = open(
        filename + '.txt',
        mode='r',
        encoding='utf-8-sig')
    return file.read().split("\n")


def print_tree() -> None:
    if ROOT is None:
        print('ROOT=None')
    else:
        print(json.dumps(convert_tree_to_json(ROOT), indent=2))


def crash(law: List[str], i: int, error_message: str) -> None:
    print_tree()
    print_around(law, i)
    raise Exception(error_message)


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

    parse_undang_undang(law)

    assert ROOT is not None
    with open(filename + '.json', 'w') as outfile:
        json.dump(
            convert_tree_to_json(ROOT),
            outfile,
            indent=2
        )
