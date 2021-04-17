#!/usr/bin/env python3
import json
import sys
from typing import Any, Dict, List, Tuple, Union

from parser_types import (
    NORMAL_LIST_INDEX_STRUCTURES,
    PENJELASAN_LIST_INDEX_STRUCTURES,
    PlaintextInListItemScenario,
    Structure,
    TEXT_BLOCK_STRUCTURES,
    PRIMITIVE_STRUCTURES,
    PrimitiveNode,
    ComplexNode
)
from parser_is_start_of_x import (
    is_start_of_lembaran_number,
    is_start_of_number_with_right_bracket,
    is_start_of_pasal,
    is_start_of_penjelasan_angka,
    is_start_of_penjelasan_ayat,
    is_start_of_penjelasan_huruf,
    is_start_of_penjelasan_list_index_str,
    is_start_of_structure,
    is_start_of_first_list_index,
    is_start_of_any,
    is_start_of_plaintext,
    is_start_of_list_item,
    is_start_of_letter_with_dot,
    is_start_of_number_with_dot,
    is_start_of_number_with_brackets,
    is_start_of_unordered_list_item,
)
from parser_utils import (
    convert_tree_to_json,
    extract_metadata_from_tree,
    gen_plaintext_in_list_item_scenario_from_user,
    get_list_index_type,
    is_next_list_index_number,
    load_clean_law,
    print_around,
)

'''
Global variable that is set to the root node of the law tree. Having global
access makes it easy to print out a snapshot of the current state of the
law tree at any point during parsing. This is useful for various use cases,
the main example of which is printing a snapshot of the law tree before
crashing to provide useful debugging clues.
'''
ROOT: Union[ComplexNode, None] = None

'''
-----------------

PARSE_X FUNCTIONS

-----------------
'''


def parse_undang_undang(root: ComplexNode, law: List[str]):
    """
    Construct a tree that represents the law as a hierarchy of nodes.

    Representing the tree using JSON, this is an e.g of what the root node will
    be before/after this function is executed

    Before

    >>> {
    >>>     type: UNDANG_UNDANG
    >>>     children: []
    >>> }

    After

    >>> {
    >>>     type: UNDANG_UNDANG
    >>>     children: [
    >>>         { type: OPENING, children: [...] },
    >>>         { type: BAB, children: [...] }, # BAB 1
    >>>         { type: BAB, children: [...] }, # BAB 2
    >>>         { type: BAB, children: [...] }, # BAB 3
    >>>         ...
    >>>     ]
    >>> }

    Args:
        root: The root node of the law tree; when passed in the root node should have
        no children. This function will add child & ancestor nodes to the root node
        as the law is parsed.

        law: Ordered list of strings that contain the text of the law we want to parse
    """
    end_index = parse_opening(root, law, 0)
    start_index = end_index+1

    child_structure = Structure.BAB
    if is_start_of_pasal(law, start_index):
        '''
        From UU 1 1928 Tentang Konvensi Vina, which is so short it just has PASALs without BABs
        '''
        child_structure = Structure.PASAL

    end_index = parse_complex_structure(
        root,
        law,
        start_index,
        ancestor_structures=[],
        sibling_structures=[Structure.PENJELASAN],
        child_structures=[child_structure, Structure.CLOSING],
    )

    _ = parse_penjelasan(root, law, start_index=end_index+1)


def parse_opening(parent: ComplexNode, law: List[str], start_index: int) -> int:
    """
    Construct a subtree of nodes that represents the OPENING section of a law.

    e.g given the following law & start_index

    >>> [
    >>>     "UNDANG-UNDANG REPUBLIK INDONESIA ", <-- start_index
    >>>     "NOMOR 14 TAHUN 2008 ",
    >>>     ...,
    >>>     "Menimbang: ",
    >>>     "a.",
    >>>     "bahwa informasi merupakan kebutuhan pokok setiap orang bagi pengembangan pribadi dan lingkungan sosialnya serta merupakan bagian penting bagi ketahanan nasional;",
    >>>     "b.",
    >>>     ...,
    >>>     "Menetapkan: ",
    >>>     "UNDANG-UNDANG TENTANG KETERBUKAAN INFORMASI PUBLIK ",
    >>>     ...,
    >>> ]

    the subtree constructed will look like this

    >>> {
    >>>     type: OPENING
    >>>     children: [
    >>>         { type: UU_TITLE, children: [...] },
    >>>         { type: PREFACE, children: [...] },
    >>>         { type: CONSIDERATIONS, children: [...] },
    >>>         { type: PRINCIPLES, children: [...] },
    >>>         { type: AGREEMENT, children: [...] },
    >>>     ]
    >>> }

    and the return value will mark the end_index; i.e the last line of the OPENING

    >>> [
    >>>     "UNDANG-UNDANG REPUBLIK INDONESIA ", <-- start_index
    >>>     "NOMOR 14 TAHUN 2008 ",
    >>>     ...,
    >>>     "Menimbang: ",
    >>>     "a.",
    >>>     "bahwa informasi merupakan kebutuhan pokok setiap orang bagi pengembangan pribadi dan lingkungan sosialnya serta merupakan bagian penting bagi ketahanan nasional;",
    >>>     "b.",
    >>>     ...,
    >>>     "Menetapkan: ",
    >>>     "UNDANG-UNDANG TENTANG KETERBUKAAN INFORMASI PUBLIK ", <-- end_index
    >>>     ...,
    >>> ]

    Args:
        parent: the parent node of the subtree that represents the OPENING of a law;
        the subtree is attached to the parent node passed in.

        law: Ordered list of strings that contain the text of the law we want to parse
        start_index: law[start_index] is the 1st line of the OPENING we want to parse

    Returns:
        int: the end_index; i.e law[end_index] is the last line of the OPENING we want to parse
    """
    opening_node = ComplexNode(type=Structure.OPENING)
    parent.add_child(opening_node)

    end_index = parse_uu_title(opening_node, law, start_index)
    end_index = parse_preface(opening_node, law, start_index=end_index+1)
    end_index = parse_considerations(
        opening_node, law, start_index=end_index+1)
    end_index = parse_principles(opening_node, law, start_index=end_index+1)
    end_index = parse_agreement(opening_node, law, start_index=end_index+1)

    return end_index


def parse_uu_title(parent: ComplexNode, law: List[str], start_index: int) -> int:
    """
    Construct a subtree of nodes that represents the UU_TITLE section of a law.

    e.g given the following law & start_index

    >>> [
    >>>     "UNDANG-UNDANG REPUBLIK INDONESIA ", <-- start_index
    >>>     "NOMOR 14 TAHUN 2008 ",
    >>>     "TENTANG ",
    >>>     "KETERBUKAAN INFORMASI PUBLIK ",
    >>>     ...,
    >>> ]

    the subtree constructed will look like this

    >>> {
    >>>     type: UU_TITLE
    >>>     children: [
    >>>         { type: PLAINTEXT, text: 'UNDANG-UNDANG REPUBLIK INDONESIA' },
    >>>         { type: UU_TITLE_YEAR_AND_NUMBER, text: 'NOMOR 14 TAHUN 2008' },
    >>>         { type: PLAINTEXT, text: 'TENTANG' },
    >>>         { type: UU_TITLE_TOPIC, text: 'KETERBUKAAN INFORMASI PUBLIK' },
    >>>     ]
    >>> }

    and the return value will mark the end_index; i.e the last line of the UU_TITLE

    >>> [
    >>>     "UNDANG-UNDANG REPUBLIK INDONESIA ", <-- start_index
    >>>     "NOMOR 14 TAHUN 2008 ",
    >>>     "TENTANG ",
    >>>     "KETERBUKAAN INFORMASI PUBLIK ", <-- end_index
    >>>     ...,
    >>> ]

    Args:
        parent: the parent node of the subtree that represents the UU_TITLE of a law;
        the subtree is attached to the parent node passed in.

        law: Ordered list of strings that contain the text of the law we want to parse
        start_index: law[start_index] is the 1st line of the UU_TITLE we want to parse

    Returns:
        int: the end_index; i.e law[end_index] is the last line of the UU_TITLE we want to parse
    """
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
    """
    Construct a subtree of nodes that represents the PREFACE section of a law.

    e.g given the following law & start_index

    >>> [
    >>>     ...,
    >>>     "DENGAN RAHMAT TUHAN YANG MAHA ESA ", <-- start_index
    >>>     "PRESIDEN REPUBLIK INDONESIA, ",
    >>>     ...,
    >>> ]

    the subtree constructed will look like this

    >>> {
    >>>     type: PREFACE
    >>>     children: [
    >>>         { type: PLAINTEXT, text: 'DENGAN RAHMAT TUHAN YANG MAHA ESA' },
    >>>         { type: PLAINTEXT, text: 'PRESIDEN REPUBLIK INDONESIA, ' },
    >>>     ]
    >>> }

    and the return value will mark the end_index; i.e the last line of the PREFACE

    >>> [
    >>>     ...,
    >>>     "DENGAN RAHMAT TUHAN YANG MAHA ESA ", <-- start_index
    >>>     "PRESIDEN REPUBLIK INDONESIA, ", <-- end_index
    >>>     ...,
    >>> ]

    Args:
        parent: the parent node of the subtree that represents the PREFACE of a law;
        the subtree is attached to the parent node passed in.

        law: Ordered list of strings that contain the text of the law we want to parse
        start_index: law[start_index] is the 1st line of the PREFACE we want to parse

    Returns:
        int: the end_index; i.e law[end_index] is the last line of the PREFACE we want to parse
    """
    preface_node = ComplexNode(type=Structure.PREFACE)
    parent.add_child(preface_node)

    preface_node.add_child(PrimitiveNode(
        type=Structure.PLAINTEXT, text=law[start_index]))
    preface_node.add_child(PrimitiveNode(
        type=Structure.PLAINTEXT, text=law[start_index+1]))

    end_index = start_index+1
    return end_index


def parse_considerations(parent: ComplexNode, law: List[str], start_index: int) -> int:
    """
    Construct a subtree of nodes that represents the CONSIDERATIONS section of a law.

    e.g given the following law & start_index

    >>> [
    >>>     ...,
    >>>     "Menimbang: ", <-- start_index
    >>>     "a.",
    >>>     "bahwa informasi merupakan kebutuhan pokok setiap orang...",
    >>>     "b.",
    >>>     "bahwa hak memperoleh informasi merupakan hak asasi manusia...",
    >>>     ...,
    >>> ]

    the subtree constructed will look like this

    >>> {
    >>>     type: CONSIDERATIONS
    >>>     children: [
    >>>         { type: PLAINTEXT, text: 'Menimbang:' },
    >>>         { type: LIST, children: [...] },
    >>>     ]
    >>> }

    and the return value will mark the end_index; i.e the last line of the CONSIDERATIONS

    >>> [
    >>>     ...,
    >>>     "Menimbang: ", <-- start_index
    >>>     "a.",
    >>>     "bahwa informasi merupakan kebutuhan pokok setiap orang...",
    >>>     "b.",
    >>>     "bahwa hak memperoleh informasi merupakan hak asasi manusia...", <-- end_index
    >>>     ...,
    >>> ]

    Args:
        parent: the parent node of the subtree that represents the CONSIDERATIONS of a law;
        the subtree is attached to the parent node passed in.

        law: Ordered list of strings that contain the text of the law we want to parse
        start_index: law[start_index] is the 1st line of the CONSIDERATIONS we want to parse

    Returns:
        int: the end_index; i.e law[end_index] is the last line of the CONSIDERATIONS we want to parse
    """
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
        sibling_structures=[Structure.PRINCIPLES],
        child_structures=TEXT_BLOCK_STRUCTURES,
    )

    return end_index


def parse_principles(parent: ComplexNode, law: List[str], start_index: int) -> int:
    """
    Construct a subtree of nodes that represents the PRINCIPLES section of a law.

    e.g given the following law & start_index

    >>> [
    >>>     ...,
    >>>     "Mengingat: ", <-- start_index
    >>>     "Pasal 20 UUD Negara Republik Indonesia Tahun 1945. ",
    >>>     ...,
    >>> ]

    the subtree constructed will look like this

    >>> {
    >>>     type: PRINCIPLES
    >>>     children: [
    >>>         { type: PLAINTEXT, text: 'Mengingat:' },
    >>>         { type: PLAINTEXT, text: 'Pasal 20 UUD Negara Republik Indonesia Tahun 1945.' },
    >>>     ]
    >>> }

    and the return value will mark the end_index; i.e the last line of the PRINCIPLES

    >>> [
    >>>     ...,
    >>>     "Mengingat: ", <-- start_index
    >>>     "Pasal 20 UUD Negara Republik Indonesia Tahun 1945. ", <-- end_index
    >>>     ...,
    >>> ]

    Args:
        parent: the parent node of the subtree that represents the PRINCIPLES of a law;
        the subtree is attached to the parent node passed in.

        law: Ordered list of strings that contain the text of the law we want to parse
        start_index: law[start_index] is the 1st line of the PRINCIPLES we want to parse

    Returns:
        int: the end_index; i.e law[end_index] is the last line of the PRINCIPLES we want to parse
    """
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
    """
    Construct a subtree of nodes that represents the AGREEMENT section of a law.

    e.g given the following law & start_index

    >>> [
    >>>     ...,
    >>>     "Dengan Persetujuan Bersama: ", <-- start_index
    >>>     "DEWAN PERWAKILAN RAKYAT REPUBLIK INDONESIA ",
    >>>     "dan ",
    >>>     "PRESIDEN REPUBLIK INDONESIA ",
    >>>     "MEMUTUSKAN: ",
    >>>     "Menetapkan: ",
    >>>     "UNDANG-UNDANG TENTANG KETERBUKAAN INFORMASI PUBLIK ",
    >>>     ...,
    >>> ]

    the subtree constructed will look like this

    >>> {
    >>>     type: AGREEMENT
    >>>     children: [
    >>>         { type: PLAINTEXT, text: 'Dengan Persetujuan Bersama:' },
    >>>         { type: PLAINTEXT, text: 'DEWAN PERWAKILAN RAKYAT REPUBLIK INDONESIA' },
    >>>         { type: PLAINTEXT, text: 'dan' },
    >>>         { type: PLAINTEXT, text: 'PRESIDEN REPUBLIK INDONESIA' },
    >>>         { type: PLAINTEXT, text: 'Dengan Persetujuan Bersama:' },
    >>>         { type: PLAINTEXT, text: 'MEMUTUSKAN:' },
    >>>         { type: PLAINTEXT, text: 'Menetapkan:' },
    >>>         { type: PLAINTEXT, text: 'UNDANG-UNDANG TENTANG KETERBUKAAN INFORMASI PUBLIK' },
    >>>     ]
    >>> }

    and the return value will mark the end_index; i.e the last line of the AGREEMENT

    >>> [
    >>>     ...,
    >>>     "Dengan Persetujuan Bersama: ", <-- start_index
    >>>     "DEWAN PERWAKILAN RAKYAT REPUBLIK INDONESIA ",
    >>>     "dan ",
    >>>     "PRESIDEN REPUBLIK INDONESIA ",
    >>>     "MEMUTUSKAN: ",
    >>>     "Menetapkan: ",
    >>>     "UNDANG-UNDANG TENTANG KETERBUKAAN INFORMASI PUBLIK ", <-- end_index
    >>>     ...,
    >>> ]

    Args:
        parent: the parent node of the subtree that represents the AGREEMENT of a law;
        the subtree is attached to the parent node passed in.

        law: Ordered list of strings that contain the text of the law we want to parse
        start_index: law[start_index] is the 1st line of the AGREEMENT we want to parse

    Returns:
        int: the end_index; i.e law[end_index] is the last line of the AGREEMENT we want to parse
    """
    agreement_node = ComplexNode(type=Structure.AGREEMENT)
    parent.add_child(agreement_node)

    i = 0
    while "menetapkan:" not in law[start_index+i].lower():
        agreement_node.add_child(PrimitiveNode(
            type=Structure.PLAINTEXT, text=law[start_index+i]))
        i += 1

    # AGREEMENT always ends w/ a "Menetapkan:" line followed by a line w/ the name of the law
    agreement_node.add_child(PrimitiveNode(
        type=Structure.PLAINTEXT, text=law[start_index+i]))
    agreement_node.add_child(PrimitiveNode(
        type=Structure.PLAINTEXT, text=law[start_index+i+1]))

    end_index = start_index+i+1
    return end_index


def parse_bab(parent: ComplexNode, law: List[str], start_index: int) -> int:
    """
    Construct a subtree of nodes that represents the BAB section of a law.

    e.g given the following law & start_index

    >>> [
    >>>     ...,
    >>>     "BAB VI ", <-- start_index
    >>>     "MEKANISME MEMPEROLEH INFORMASI ",
    >>>     "Pasal 21 ",
    >>>     "Mekanisme untuk memperoleh Informasi Publik...",
    >>>     ...,
    >>>     "Ketentuan lebih lanjut mengenai...",
    >>>     "BAB VII ",
    >>>     ...,
    >>> ]

    the subtree constructed will look like this

    >>> {
    >>>     type: BAB
    >>>     children: [
    >>>         { type: BAB_NUMBER, text: 'BAB VI' },
    >>>         { type: BAB_TITLE, text: 'MEKANISME MEMPEROLEH INFORMASI' },
    >>>         { type: PASAL, children: [...] }, # Pasal 21
    >>>         { type: PASAL, children: [...] }, # Pasal 22
    >>>         { type: PASAL, children: [...] }, # Pasal 23
    >>>         ...,
    >>>     ]
    >>> }

    and the return value will mark the end_index; i.e the last line of the BAB

    >>> [
    >>>     ...,
    >>>     "BAB VI ", <-- start_index
    >>>     "MEKANISME MEMPEROLEH INFORMASI ",
    >>>     "Pasal 21 ",
    >>>     "Mekanisme untuk memperoleh Informasi Publik...",
    >>>     ...,
    >>>     "Ketentuan lebih lanjut mengenai...", <-- end_index
    >>>     "BAB VII ",
    >>>     ...,
    >>> ]

    Args:
        parent: the parent node of the subtree that represents the BAB of a law;
        the subtree is attached to the parent node passed in.

        law: Ordered list of strings that contain the text of the law we want to parse
        start_index: law[start_index] is the 1st line of the BAB we want to parse

    Returns:
        int: the end_index; i.e law[end_index] is the last line of the BAB we want to parse
    """
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
        sibling_structures=[Structure.BAB,
                            Structure.CLOSING, Structure.PENJELASAN],
        child_structures=[Structure.PASAL, Structure.BAGIAN])

    return end_index


def parse_pasal(parent: ComplexNode, law: List[str], start_index: int) -> int:
    """
    Construct a subtree of nodes that represents the PASAL section of a law.

    e.g given the following law & start_index

    >>> [
    >>>     ...,
    >>>     "Pasal 35", <-- start_index
    >>>     "(1)",
    >>>     "Setiap Pemohon Informasi Publik dapat mengajukan...",
    >>>     ...,
    >>>     "Alasan sebagaimana dimaksud...",
    >>>     "Pasal 36",
    >>>     ...,
    >>> ]

    the subtree constructed will look like this

    >>> {
    >>>     type: PASAL
    >>>     children: [
    >>>         { type: PASAL_NUMBER, text: 'Pasal 35' },
    >>>         { type: LIST, children: [...] },
    >>>     ]
    >>> }

    and the return value will mark the end_index; i.e the last line of the PASAL

    >>> [
    >>>     ...,
    >>>     "Pasal 35", <-- start_index
    >>>     "(1)",
    >>>     "Setiap Pemohon Informasi Publik dapat mengajukan...",
    >>>     ...,
    >>>     "Alasan sebagaimana dimaksud...", <-- end_index
    >>>     "Pasal 36",
    >>>     ...,
    >>> ]

    Args:
        parent: the parent node of the subtree that represents the PASAL of a law;
        the subtree is attached to the parent node passed in.

        law: Ordered list of strings that contain the text of the law we want to parse
        start_index: law[start_index] is the 1st line of the PASAL we want to parse

    Returns:
        int: the end_index; i.e law[end_index] is the last line of the PASAL we want to parse
    """
    pasal_node = ComplexNode(type=Structure.PASAL)
    parent.add_child(pasal_node)

    pasal_node.add_child(PrimitiveNode(
        type=Structure.PASAL_NUMBER, text=law[start_index]))

    end_index = parse_complex_structure(
        pasal_node,
        law,
        start_index+1,
        ancestor_structures=[
            Structure.BAB,
            Structure.BAGIAN,
            Structure.PARAGRAF,
            Structure.CLOSING,
            Structure.PENJELASAN
        ],
        sibling_structures=[Structure.PASAL],
        child_structures=TEXT_BLOCK_STRUCTURES)

    return end_index


def parse_bagian(parent: ComplexNode, law: List[str], start_index: int) -> int:
    """
    Construct a subtree of nodes that represents the BAGIAN section of a law.

    e.g given the following law & start_index

    >>> [
    >>>     ...,
    >>>     "Bagian Kesatu", <-- start_index
    >>>     "Asas",
    >>>     "Pasal 7",
    >>>     ...,
    >>>     "Informasi Publik yang dikecualikan...",
    >>>     "Bagian Kedua",
    >>>     ...,
    >>> ]

    the subtree constructed will look like this

    >>> {
    >>>     type: BAGIAN
    >>>     children: [
    >>>         { type: BAGIAN_NUMBER, text: 'Bagian Kesatu' },
    >>>         { type: BAGIAN_TITLE, text: 'Asas' },
    >>>         { type: PASAL, children: [...] }, # Pasal 7
    >>>         { type: PASAL, children: [...] }, # Pasal 8
    >>>         ...,
    >>>     ]
    >>> }

    and the return value will mark the end_index; i.e the last line of the BAGIAN

    >>> [
    >>>     ...,
    >>>     "Bagian Kesatu", <-- start_index
    >>>     "Asas",
    >>>     "Pasal 7",
    >>>     ...,
    >>>     "Informasi Publik yang dikecualikan...", <-- end_index
    >>>     "Bagian Kedua",
    >>>     ...,
    >>> ]

    Args:
        parent: the parent node of the subtree that represents the BAGIAN of a law;
        the subtree is attached to the parent node passed in.

        law: Ordered list of strings that contain the text of the law we want to parse
        start_index: law[start_index] is the 1st line of the BAGIAN we want to parse

    Returns:
        int: the end_index; i.e law[end_index] is the last line of the BAGIAN we want to parse
    """
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
        ancestor_structures=[
            Structure.BAB,
            Structure.CLOSING,
            Structure.PENJELASAN,
        ],
        sibling_structures=[Structure.BAGIAN],
        child_structures=[Structure.PASAL, Structure.PARAGRAF])

    return end_index


def parse_paragraf(parent: ComplexNode, law: List[str], start_index: int) -> int:
    """
    Construct a subtree of nodes that represents the PARAGRAF section of a law.

    e.g given the following law & start_index

    >>> [
    >>>     ...,
    >>>     "Paragraf 2", <-- start_index
    >>>     "Perizinan Berusaha",
    >>>     "Pasal 10",
    >>>     ...,
    >>>     "Informasi Publik yang dikecualikan...",
    >>>     "Paragraf 3",
    >>>     ...,
    >>> ]

    the subtree constructed will look like this

    >>> {
    >>>     type: PARAGRAF
    >>>     children: [
    >>>         { type: PARAGRAF_NUMBER, text: 'Paragraf 2' },
    >>>         { type: PARAGRAF_TITLE, text: 'Perizinan Berusaha' },
    >>>         { type: PASAL, children: [...] }, # Pasal 10
    >>>         ...,
    >>>     ]
    >>> }

    and the return value will mark the end_index; i.e the last line of the PARAGRAF

    >>> [
    >>>     ...,
    >>>     "Paragraf 2", <-- start_index
    >>>     "Perizinan Berusaha",
    >>>     "Pasal 10",
    >>>     ...,
    >>>     "Informasi Publik yang dikecualikan...",
    >>>     "Paragraf 3", <-- end_index
    >>>     ...,
    >>> ]

    Args:
        parent: the parent node of the subtree that represents the PARAGRAF of a law;
        the subtree is attached to the parent node passed in.

        law: Ordered list of strings that contain the text of the law we want to parse
        start_index: law[start_index] is the 1st line of the PARAGRAF we want to parse

    Returns:
        int: the end_index; i.e law[end_index] is the last line of the PARAGRAF we want to parse
    """
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
        ancestor_structures=[
            Structure.BAB,
            Structure.BAGIAN,
            Structure.CLOSING,
            Structure.PENJELASAN,
        ],
        sibling_structures=[Structure.PARAGRAF],
        child_structures=[Structure.PASAL])

    return end_index


def parse_list(parent: ComplexNode, law: List[str], start_index: int) -> int:
    """
    Construct a subtree of nodes that represents the LIST section of a law.

    e.g given the following law & start_index

    >>> [
    >>>     ...,
    >>>     "a.", <-- start_index
    >>>     "asas dan tujuan;",
    >>>     "b.",
    >>>     "program dan kegiatan organisasi;",
    >>>     "c.",
    >>>     "nama, alamat, susunan kepengurusan, dan perubahannya;",
    >>>     "BAB V ",
    >>>     ...,
    >>> ]

    the subtree constructed will look like this

    >>> {
    >>>     type: LIST
    >>>     children: [
    >>>         { type: LIST_ITEM, children: [...] }, # a.
    >>>         { type: LIST_ITEM, children: [...] }, # b.
    >>>         { type: LIST_ITEM, children: [...] }, # c.
    >>>     ]
    >>> }

    and the return value will mark the end_index; i.e the last line of the LIST

    >>> [
    >>>     ...,
    >>>     "a.", <-- start_index
    >>>     "asas dan tujuan;",
    >>>     "b.",
    >>>     "program dan kegiatan organisasi;",
    >>>     "c.",
    >>>     "nama, alamat, susunan kepengurusan, dan perubahannya;", <-- end_index
    >>>     "BAB V ",
    >>>     ...,
    >>> ]

    Args:
        parent: the parent node of the subtree that represents the LIST of a law;
        the subtree is attached to the parent node passed in.

        law: Ordered list of strings that contain the text of the law we want to parse
        start_index: law[start_index] is the 1st line of the LIST we want to parse

    Returns:
        int: the end_index; i.e law[end_index] is the last line of the LIST we want to parse
    """

    '''
    in parse_list, we might run into ancestor lists, but not child lists, because
    any child lists should be embedded inside a list item
    '''
    list_node = ComplexNode(type=Structure.LIST)
    parent.add_child(list_node)

    non_recursive_ancestors = [
        Structure.PRINCIPLES,
        Structure.AGREEMENT,
        Structure.PASAL,
        Structure.PARAGRAF,
        Structure.BAGIAN,
        Structure.BAB,
        Structure.CLOSING,
        Structure.PENJELASAN,
        Structure.PENJELASAN_PASAL_DEMI_PASAL,
    ]
    sibling_ancestors = [Structure.PLAINTEXT]

    initial_start_index = start_index
    end_index = start_index-1
    while end_index < len(law)-1:
        not_first_line = start_index > initial_start_index
        start_of_ancestor_or_sibling = is_start_of_any(
            non_recursive_ancestors+sibling_ancestors,
            law,
            start_index
        )
        if not_first_line and start_of_ancestor_or_sibling:
            return end_index

        # if plaintext, could be child of list, or sibling of list

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
        list_index_type = get_list_index_type(law[start_index])
        if list_index_type in NORMAL_LIST_INDEX_STRUCTURES:
            end_index = parse_list_item(list_node, law, start_index)
        elif list_index_type in PENJELASAN_LIST_INDEX_STRUCTURES:
            end_index = parse_penjelasan_list_item(list_node, law, start_index)
        else:
            crash(law, start_index, 'Not a list index')

        start_index = end_index + 1

    return end_index


def parse_penjelasan_list_item(parent: ComplexNode, law: List[str], start_index: int) -> int:
    '''
    TODO(johnamadeo)

    This doesn't work for nested LIST w/ PENJELASAN_LIST_ITEM when
    the line after the LIST_INDEX is NOT the start of the nested LIST
    w/ PENJELASAN_LIST_ITEM

    (e.g try it on Pasal 53 in PENJELASAN of UU 40 2007)
    '''
    penjelasan_list_item_node = ComplexNode(
        type=Structure.PENJELASAN_LIST_ITEM)
    parent.add_child(penjelasan_list_item_node)

    parse_list_index(penjelasan_list_item_node, law, start_index)
    start_index += 1

    if is_start_of_penjelasan_list_index_str(law[start_index]):
        end_index = parse_list(penjelasan_list_item_node, law, start_index)
    else:
        end_index = parse_complex_structure(
            penjelasan_list_item_node,
            law,
            start_index=start_index,
            ancestor_structures=[Structure.PASAL],
            sibling_structures=[Structure.PENJELASAN_LIST_ITEM],
            child_structures=TEXT_BLOCK_STRUCTURES,
        )

    return end_index


def parse_list_item(parent: ComplexNode, law: List[str], start_index: int) -> int:
    """
    Construct a subtree of nodes that represents the LIST_ITEM section of a law.
    One interesting feature is that a LIST_ITEM can itself have a nested LIST inside of it

    e.g given the following law & start_index

    >>> [
    >>>     ...,
    >>>     "(1)", <-- start_index
    >>>     "Komisi Informasi bertugas:",
    >>>     "a.",
    >>>     "menerima, memeriksa, dan memutus permohonan penyelesaian Sengketa Informasi Publik melalui Mediasi dan/atau Ajudikasi nonlitigasi yang diajukan oleh setiap Pemohon Informasi Publik berdasarkan alasan sebagaimana dimaksud dalam Undang-Undang ini;",
    >>>     "b.",
    >>>     "menetapkan kebijakan umum pelayanan Informasi Publik; dan",
    >>>     "c.",
    >>>     "menetapkan petunjuk pelaksanaan dan petunjuk teknis.",
    >>>     "(2)",
    >>>     ...,
    >>> ]

    the subtree constructed will look like this

    >>> {
    >>>     type: LIST_ITEM
    >>>     children: [
    >>>         { type: NUMBER_WITH_BRACKETS, text: '(1)' }, # list index
    >>>         { type: PLAINTEXT, text: 'Komisi Informasi bertugas:' }
    >>>         {
    >>>             type: LIST,
    >>>             children: [
    >>>                 { type: LIST_ITEM, children: [...] }, # a. menerima...
    # b. menetapkan kebijakan...
    >>>                 { type: LIST_ITEM, children: [...] },
    # c. menetapkan petunjuk...
    >>>                 { type: LIST_ITEM, children: [...] },
    >>>             ]
    >>>         },
    >>>     ]
    >>> }

    and the return value will mark the end_index; i.e the last line of the LIST_ITEM

    >>> [
    >>>     ...,
    >>>     "(1)", <-- start_index
    >>>     "Komisi Informasi bertugas:",
    >>>     "a.",
    >>>     "menerima, memeriksa, dan memutus permohonan penyelesaian Sengketa Informasi Publik melalui Mediasi dan/atau Ajudikasi nonlitigasi yang diajukan oleh setiap Pemohon Informasi Publik berdasarkan alasan sebagaimana dimaksud dalam Undang-Undang ini;",
    >>>     "b.",
    >>>     "menetapkan kebijakan umum pelayanan Informasi Publik; dan",
    >>>     "c.",
    >>>     "menetapkan petunjuk pelaksanaan dan petunjuk teknis.", <-- end_index
    >>>     "(2)",
    >>>     ...,
    >>> ]

    Args:
        parent: the parent node of the subtree that represents the LIST_ITEM of a law;
        the subtree is attached to the parent node passed in.

        law: Ordered list of strings that contain the text of the law we want to parse
        start_index: law[start_index] is the 1st line of the LIST_ITEM we want to parse

    Returns:
        int: the end_index; i.e law[end_index] is the last line of the LIST_ITEM we want to parse
    """
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
    parse_list_index(list_item_node, law, start_index)
    list_item_node.add_child(PrimitiveNode(
        type=Structure.PLAINTEXT, text=law[start_index+1]))

    '''
    The 3rd line can be one of 2 scenarios.
    
    Scenario 1
    ----------- 
    The 3rd line is actually not part of the list, but marks the start of a sibling or ancestor structure of the LIST

    e.g UU 8 1997 Tentang Dokumen Perusahaan
    Pasal 18
    (1) 
    Dokumen perusahaan...
    (2) 
    Penyerahan sebagaimana...
        a.
        ...
        b.
        ...
        c.
        ...
    (3) 
    Pada berita acara...
    Pasal 19 <-- 3RD LINE

    Scenario 2
    -----------
    The 3rd line marks the start of a child of the LIST_ITEM (almost always a nested list/nested unordered list)

    e.g UU 8 1997 Tentang Dokumen Perusahaan
    Pasal 18
    (1)
    Dokumen perusahaan tertentu...
    (2) 
    Penyerahan sebagaimana...
        a. <---- 3RD LINE
        keterangan tempat...
        b. 
        keterangan tentang...
    '''

    non_recursive_ancestors = [
        Structure.PASAL,
        Structure.PARAGRAF,
        Structure.BAGIAN,
        Structure.BAB,
        Structure.PRINCIPLES,
        Structure.AGREEMENT,
        Structure.CLOSING,
        Structure.PENJELASAN,
        Structure.PENJELASAN_PASAL_DEMI_PASAL,
    ]

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
        if is_start_of_plaintext(law, start_index):
            '''
            If the 3rd line is PLAINTEXT, it could be:
            a) Sibling of the LIST the LIST_ITEM is in
            b) child of the LIST_ITEM
            c) an embedded law snippet

            The most common occurrence of a) is when the LIST itself is part of a
            sentence, and there's another PLAINTEXT after the LIST to complete the sentence.

            Example a): Sibling of the LIST the LIST_ITEM is in
            ----------------------------------------
            e.g UU 8 1997 Tentang Dokumen Perusahaan

            Pasal 30
                Pada saat Undang-undang ini mulai berlaku:
                    1. 
                    Pasal 6 Kitab Undang-undang Hukum Dagang (Wetboek van Koophandel voor Indonesië, Staatsblad  1847 : 23); dan
                    2. 
                    semua peraturan perundang-undangan yang berkaitan dengan dokumen perusahaan dan ketentuan  peraturan perundang-undangan yang berkaitan dengan penyimpanan, pemindahan, penyerahan, dan  pemusnahan arsip yang bertentangan dengan Undang-undang ini,
                dinyatakan tidak berlaku lagi. <----

            e.g UU 20 2007 Tentang Perseroan Terbatas
            Pasal 102
                (1)
                Direksi wajib meminta persetujuan RUPS untuk:
                    a.
                    mengalihkan kekayaan Perseroan; atau
                    b.
                    menjadikan jaminan utang kekayaan Perseroan;
                yang merupakan lebih dari 50% (lima puluh persen) jumlah kekayaan bersih Perseroan  dalam 1 (satu) transaksi atau lebih, baik yang berkaitan satu sama lain maupun tidak. <----

            Example c): An embedded law snippet
            ----------------------------------------
            The snippet below is a pattern found in UU that modify other UU. Pasal 17 of this UU is modifying
            Pasal 1 of another UU. Hence, the line " 'Pasal 1 " is a plaintext.

            e.g UU 11 2020 Tentang Cipta Kerja

            Pasal 17

            Beberapa ketentuan dalam Undang-Undang Nomor 26 Tahun 2007 tentang Penataan Ruang... diubah sebagai berikut:

            1. 
            Ketentuan Pasal 1 angka 7, angka 8, dan angka 32 diubah sehingga Pasal 1 berbunyi sebagai berikut:
                'Pasal 1
                    Dalam Undang-Undang ini yang dimaksud dengan:
                        1. 
                        Ruang adalah wadah yang meliputi ruang darat...
            '''
            scenario = gen_plaintext_in_list_item_scenario_from_user(
                law,
                start_index,
            )

            if scenario == PlaintextInListItemScenario.SIBLING_OF_LIST:
                return end_index
            elif scenario == PlaintextInListItemScenario.CHILD_OF_LIST_ITEM:
                child_structure = Structure.PLAINTEXT
            elif scenario == PlaintextInListItemScenario.EMBEDDED_LAW_SNIPPET:
                crash(
                    law,
                    start_index,
                    f'TODO(johnamadeo): Implement handling of embedded law snippets on line: {law[start_index]}'
                )
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
        elif is_start_of_unordered_list_item(law, start_index):
            child_structure = Structure.UNORDERED_LIST

        if child_structure == None:
            crash(law, start_index,
                  'parse_list_item: child is neither a list or plaintext')

        assert child_structure is not None  # mypy type hint
        end_index = parse_structure(
            list_item_node, child_structure, law, start_index)

        start_index = end_index + 1

    return end_index


def parse_list_index(parent: ComplexNode, law: List[str], i: int) -> None:
    """
    Construct a primitive node that represents the LIST_INDEX section of a law. 
    The primitive node's type will be one of NUMBER_WITH_BRACKETS, NUMBER_WITH_DOT
    or LETTER_WITH_DOT based on the text e.g '(11)', '11.', and 'g.'

    e.g given the following law & i

    >>> [
    >>>     ...,
    >>>     "(11)", <-- i
    >>>     ...,
    >>> ]

    the primitive node constructed will look like this

    >>> { type: NUMBER_WITH_BRACKETS, text: '(11)' }

    Args:
        parent: the parent node of the primitive node that represents the LIST_INDEX of a law;
        the primitive node is attached to the parent node passed in.

        law: Ordered list of strings that contain the text of the law we want to parse
        i: law[i] is the line containing the LIST_INDEX we want to parse
    """

    if is_start_of_letter_with_dot(law, i):
        parent.add_child(PrimitiveNode(
            type=Structure.LETTER_WITH_DOT, text=law[i]))
    elif is_start_of_number_with_dot(law, i):
        parent.add_child(PrimitiveNode(
            type=Structure.NUMBER_WITH_DOT, text=law[i]))
    elif is_start_of_number_with_brackets(law, i):
        parent.add_child(PrimitiveNode(
            type=Structure.NUMBER_WITH_BRACKETS, text=law[i]))
    elif is_start_of_number_with_right_bracket(law, i):
        parent.add_child(PrimitiveNode(
            type=Structure.NUMBER_WITH_RIGHT_BRACKET, text=law[i]))
    elif is_start_of_penjelasan_ayat(law, i):
        parent.add_child(PrimitiveNode(
            type=Structure.PENJELASAN_AYAT, text=law[i]))
    elif is_start_of_penjelasan_huruf(law, i):
        parent.add_child(PrimitiveNode(
            type=Structure.PENJELASAN_HURUF, text=law[i]))
    elif is_start_of_penjelasan_angka(law, i):
        parent.add_child(PrimitiveNode(
            type=Structure.PENJELASAN_ANGKA, text=law[i]))
    else:
        crash(law, i, f'line {i} is not a list index')


def parse_closing(parent: ComplexNode, law: List[str], start_index: int) -> int:
    """
    Construct a subtree of nodes that represents the CLOSING section of a law.

    e.g given the following law & start_index

    >>> [
    >>>     ...,
    >>>     "Disahkan Di Jakarta,", <-- start_index
    >>>     "Pada Tanggal 25 Maret 2003",
    >>>     "PRESIDEN REPUBLIK INDONESIA,",
    >>>     "Ttd.",
    >>>     "MEGAWATI SOEKARNOPUTRI",
    >>>     "Diundangkan Di Jakarta,",
    >>>     "Pada Tanggal 25 Maret 2003",
    >>>     "SEKRETARIS NEGARA REPUBLIK INDONESIA,",
    >>>     "Ttd.",
    >>>     "BAMBANG KESOWO",
    >>>     "LEMBARAN NEGARA REPUBLIK INDONESIA TAHUN 2003 NOMOR 39",
    >>>     ...,
    >>> ]

    the subtree constructed will look like this

    >>> {
    >>>     type: CLOSING
    >>>     children: [
    >>>         { type: PLAINTEXT, text: 'Disahkan Di Jakarta,' },
    >>>         { type: PLAINTEXT, text: 'Pada Tanggal 12 Agustus 2011' },
    >>>         { type: PLAINTEXT, text: 'PRESIDEN REPUBLIK INDONESIA,' },
    >>>         { type: PLAINTEXT, text: 'Ttd.' },
    >>>         { type: PLAINTEXT, text: 'DR. H. SUSILO BAMBANG YUDHOYONO' },
    >>>         { type: PLAINTEXT, text: 'Diundangkan Di Jakarta' },
    >>>         { type: PLAINTEXT, text: 'Pada Tanggal 12 Agustus 2011' },
    >>>         { type: PLAINTEXT, text: 'MENTERI HUKUM DAN HAK ASASI MANUSIA REPUBLIK INDONESIA,' },
    >>>         { type: PLAINTEXT, text: 'Ttd.' },
    >>>         { type: PLAINTEXT, text: 'PATRIALIS AKBAR' },
    >>>         { type: LEMBARAN_NUMBER, text: 'LEMBARAN NEGARA REPUBLIK INDONESIA TAHUN 2011 NOMOR 82' },
    >>>     ]
    >>> }

    and the return value will mark the end_index; i.e the last line of the CLOSING

    >>> [
    >>>     ...,
    >>>     "Disahkan Di Jakarta,", <-- start_index
    >>>     "Pada Tanggal 25 Maret 2003",
    >>>     "PRESIDEN REPUBLIK INDONESIA,",
    >>>     "Ttd.",
    >>>     "MEGAWATI SOEKARNOPUTRI",
    >>>     "Diundangkan Di Jakarta,",
    >>>     "Pada Tanggal 25 Maret 2003",
    >>>     "SEKRETARIS NEGARA REPUBLIK INDONESIA,",
    >>>     "Ttd.",
    >>>     "BAMBANG KESOWO",
    >>>     "LEMBARAN NEGARA REPUBLIK INDONESIA TAHUN 2003 NOMOR 39", <-- end_index
    >>>     ...,
    >>> ]

    Args:
        parent: the parent node of the subtree that represents the CLOSING of a law;
        the subtree is attached to the parent node passed in.

        law: Ordered list of strings that contain the text of the law we want to parse
        start_index: law[start_index] is the 1st line of the CLOSING we want to parse

    Returns:
        int: the end_index; i.e law[end_index] is the last line of the CLOSING we want to parse
    """
    closing_node = ComplexNode(type=Structure.CLOSING)
    parent.add_child(closing_node)

    i = 0
    while not is_start_of_lembaran_number(law, start_index+i):
        closing_node.add_child(PrimitiveNode(
            type=Structure.PLAINTEXT, text=law[start_index+i]))
        i += 1

    closing_node.add_child(PrimitiveNode(
        type=Structure.LEMBARAN_NUMBER, text=law[start_index+i]))

    end_index = start_index+i
    return end_index


def parse_penjelasan(parent: ComplexNode, law: List[str], start_index: int) -> int:
    """
    TODO(@johnamadeo)
    """
    penjelasan_node = ComplexNode(type=Structure.PENJELASAN)
    parent.add_child(penjelasan_node)

    end_index = parse_penjelasan_title(penjelasan_node, law, start_index)
    end_index = parse_penjelasan_umum(
        penjelasan_node, law, start_index=end_index+1)
    end_index = parse_penjelasan_pasal_demi_pasal(
        penjelasan_node, law, start_index=end_index+1)

    return end_index


def parse_penjelasan_title(parent: ComplexNode, law: List[str], start_index: int) -> int:
    """
    Construct a subtree of nodes that represents the PENJELASAN_TITLE section of a law.

    e.g given the following law & start_index

    >>> [
    >>>     ...,
    >>>     "PENJELASAN", <-- start_index
    >>>     "UNDANG-UNDANG REPUBLIK INDONESIA ", 
    >>>     "NOMOR 14 TAHUN 2008 ",
    >>>     "TENTANG ",
    >>>     "KETERBUKAAN INFORMASI PUBLIK ",
    >>>     ...,
    >>> ]

    the subtree constructed will look like this

    >>> {
    >>>     type: PENJELASAN_TITLE
    >>>     children: [
    >>>         { type: PLAINTEXT, text: 'PENJELASAN' },
    >>>         { type: PLAINTEXT, text: 'UNDANG-UNDANG REPUBLIK INDONESIA' },
    >>>         { type: UU_TITLE_YEAR_AND_NUMBER, text: 'NOMOR 14 TAHUN 2008' },
    >>>         { type: PLAINTEXT, text: 'TENTANG' },
    >>>         { type: UU_TITLE_TOPIC, text: 'KETERBUKAAN INFORMASI PUBLIK' },
    >>>     ]
    >>> }

    and the return value will mark the end_index; i.e the last line of the PENJELASAN_TITLE

    >>> [
    >>>     ...,
    >>>     "PENJELASAN", <-- start_index
    >>>     "UNDANG-UNDANG REPUBLIK INDONESIA ",
    >>>     "NOMOR 14 TAHUN 2008 ",
    >>>     "TENTANG ",
    >>>     "KETERBUKAAN INFORMASI PUBLIK ", <-- end_index
    >>>     ...,
    >>> ]

    Args:
        parent: the parent node of the subtree that represents the PENJELASAN_TITLE of a law;
        the subtree is attached to the parent node passed in.

        law: Ordered list of strings that contain the text of the law we want to parse
        start_index: law[start_index] is the 1st line of the PENJELASAN_TITLE we want to parse

    Returns:
        int: the end_index; i.e law[end_index] is the last line of the PENJELASAN_TITLE we want to parse
    """
    penjelasan_title_node = ComplexNode(type=Structure.PENJELASAN_TITLE)
    parent.add_child(penjelasan_title_node)

    penjelasan_title_node.add_child(PrimitiveNode(
        type=Structure.PLAINTEXT, text=law[start_index]))
    penjelasan_title_node.add_child(PrimitiveNode(
        type=Structure.PLAINTEXT, text=law[start_index+1]))
    penjelasan_title_node.add_child(PrimitiveNode(type=Structure.UU_TITLE_YEAR_AND_NUMBER,
                                                  text=law[start_index+2]))
    penjelasan_title_node.add_child(PrimitiveNode(
        type=Structure.PLAINTEXT, text=law[start_index+3]))
    penjelasan_title_node.add_child(PrimitiveNode(type=Structure.UU_TITLE_TOPIC,
                                                  text=law[start_index+4]))

    end_index = start_index+4
    return end_index


def parse_penjelasan_umum(parent: ComplexNode, law: List[str], start_index: int) -> int:
    '''
    TODO(@johnamadeo)
    '''
    penjelasan_umum_node = ComplexNode(type=Structure.PENJELASAN_UMUM)
    parent.add_child(penjelasan_umum_node)

    penjelasan_umum_node.add_child(PrimitiveNode(
        type=Structure.PENJELASAN_UMUM_TITLE, text=law[start_index]))

    end_index = parse_complex_structure(
        penjelasan_umum_node,
        law,
        start_index+1,
        # TODO(johnamadeo): Clarify that this should be next ancestor strucutres
        ancestor_structures=[
        ],
        sibling_structures=[Structure.PENJELASAN_PASAL_DEMI_PASAL],
        child_structures=TEXT_BLOCK_STRUCTURES)

    return end_index


def parse_penjelasan_pasal_demi_pasal(parent: ComplexNode, law: List[str], start_index: int) -> int:
    '''
    TODO(@johnamadeo)
    '''
    penjelasan_pasal_demi_pasal = ComplexNode(
        type=Structure.PENJELASAN_PASAL_DEMI_PASAL)
    parent.add_child(penjelasan_pasal_demi_pasal)

    penjelasan_pasal_demi_pasal.add_child(PrimitiveNode(
        type=Structure.PENJELASAN_PASAL_DEMI_PASAL_TITLE, text=law[start_index]))

    if not is_start_of_pasal(law, start_index+1):
        '''
        TODO(@johnamadeo): Covers edge case where the content of PENJELASAN_PASAL_DEMI_PASAL
        is just a 'Cukup Jelas.' followed by the Tambahan Lembaran Negara number; but may need 
        to make more robust in the future if there are UU where the content is not under PASAL, 
        but still has multiple TEXT_BLOCK_STRUCTURES

        e.g UU 1 1982 Konvensi Vina
        '''
        penjelasan_pasal_demi_pasal.add_child(PrimitiveNode(
            type=Structure.PLAINTEXT, text=law[start_index+1]))
        penjelasan_pasal_demi_pasal.add_child(PrimitiveNode(
            type=Structure.PLAINTEXT, text=law[start_index+2]))
        return start_index+2

    end_index = parse_complex_structure(
        penjelasan_pasal_demi_pasal,
        law,
        start_index+1,
        ancestor_structures=[],
        sibling_structures=[],
        child_structures=[Structure.PASAL])

    return end_index


def parse_unordered_list(parent: ComplexNode, law: List[str], start_index: int) -> int:
    '''
    TODO(@johnamadeo)
    '''
    unordered_list_node = ComplexNode(type=Structure.UNORDERED_LIST)
    parent.add_child(unordered_list_node)

    end_index = start_index-1

    # naive algorithm assumes no nested unordered lists exist
    while end_index < len(law)-1:
        if not is_start_of_unordered_list_item(law, start_index):
            break

        unordered_list_item_node = ComplexNode(
            type=Structure.UNORDERED_LIST_ITEM)
        unordered_list_node.add_child(unordered_list_item_node)

        unordered_list_index_node = PrimitiveNode(
            type=Structure.UNORDERED_LIST_INDEX, text=law[start_index])
        plaintext_node = PrimitiveNode(
            type=Structure.PLAINTEXT, text=law[start_index+1])
        unordered_list_item_node.add_child(unordered_list_index_node)
        unordered_list_item_node.add_child(plaintext_node)

        end_index += 2
        start_index = end_index+1

    return end_index


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
    """
    Construct a subtree of node(s) that represents a particular section of the law,
    where the structure - in other words, the type of the section - (e.g LIST, BAB, PASAL) is 
    passed in as an argument

    Args:
        parent: the parent node of the subtree that represents the contents of;
        the subtree is attached to the parent node passed in.

        structure: the structure we want to parse e.g LIST_ITEM, BAB, OPENING

        law: Ordered list of strings that contain the text of the law we want to parse
        start_index: law[start_index] is the 1st line of the structures we want to parse

    Returns:
        int: the end_index; i.e law[end_index] is the last line of the structures we want to parse
    """
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
        parse_list_index(parent, law, start_index)
        end_index = start_index
        return end_index
    elif structure == Structure.CLOSING:
        return parse_closing(parent, law, start_index)
    elif structure == Structure.PENJELASAN:
        return parse_penjelasan(parent, law, start_index)
    elif structure == Structure.PENJELASAN_UMUM:
        return parse_penjelasan_umum(parent, law, start_index)
    elif structure == Structure.PENJELASAN_PASAL_DEMI_PASAL:
        return parse_penjelasan_pasal_demi_pasal(parent, law, start_index)
    elif structure == Structure.PENJELASAN_LIST_ITEM:
        return parse_penjelasan_list_item(parent, law, start_index)
    elif structure == Structure.UNORDERED_LIST:
        return parse_unordered_list(parent, law, start_index)
    else:
        crash(law, start_index, f'No function to parse {structure.value}')
        return -1  # only to satisfy mypy; will never run since we crash


def parse_complex_structure(
    parent: ComplexNode,
    law: List[str],
    start_index: int,
    # doesn't have to include root structure (i.e UNDANG_UNDANG)
    ancestor_structures: List[Structure],
    # TODO(johnamadeo) - rename to next_sibling_structures?
    sibling_structures: List[Structure],
    child_structures: List[Structure],
) -> int:
    """
    Given a complex parent node, construct a list of its child nodes.

    Most complex structures (e.g BAB, PASAL) don't have a fixed pre-determined length.
    For example, a BAB could consist of any number of PASALs >= 1. A PASAL could consist
    of a LIST of unknown length.

    Thus, this function employs a greedy algorithm that starts at law[start_index], and then 
    proceeds to examine each following line (start_index+1, start_index+2...) until the end of the 
    structure is detected.

    e.g for a PASAL, the algorithm will keep going until it detects a line that marks the 
    start of a different structure, perhaps i) the next PASAL or ii) the next BAB, which 
    means that the current BAB the PASAL is in is also over

    for i) the next PASAL, this might look like

    >>> [
    >>>     "Pasal 45", # <-- started here
    >>>     "(1)",
    >>>     "Badan Publik harus membuktikan hal-hal yang mendukung pendapatnya...",
    >>>     "(2)",
    >>>     "Badan Publik harus menyampaikan alasan yang mendukung sikapnya...",
    >>>     "Pasal 46 ", # <-- reached here and detected Pasal 45 is over
    >>> ]

    for ii) the next BAB, this might look like

    >>> [
    >>>     "BAB V",
    >>>     "MEKANISME MEMPEROLEH INFORMASI",
    >>>     "Pasal 21 ",
    >>>     "Mekanisme untuk memperoleh Informasi Publik didasarkan...",
    >>>     "Pasal 22", # <-- started here
    >>>     "(1)",
    >>>     "Badan Publik harus membuktikan hal-hal yang mendukung pendapatnya...",
    >>>     "(2)",
    >>>     "Badan Publik harus menyampaikan alasan yang mendukung sikapnya...",
    >>>     "BAB VI", # <-- reached here and detected Pasal 22 is over
    >>> ]

    Args:
        parent: a complex parent node; the list of child nodes constructed by this function
        will be attached to the parent node

        law: Ordered list of strings that contain the text of the law we want to parse
        start_index: law[start_index] is the line we want to start parsing from

        ancestor_structures: a list of structures that could be ancestors of the parent node;
        e.g for a PASAL, BAGIAN & PARAGRAF are structures that could be an ancestor of PASAL

        sibling_structures: a list of structures that could be siblings to the parent node;
        e.g a PASAL can be a sibling to other PASALs (e.g Pasal 2 follows Pasal 1), 
        PRINCIPLES is a sibling to CONSIDERATIONS

        child_structures: a list of structures that could be children to the parent node;
        e.g a BAB can have BAGIAN, PARAGRAF, and PASAL as its children

    Returns:
        int: the end_index; i.e law[end_index] is the last line of the structure we want to parse
    """

    if parent.type in set([
            Structure.LIST,
            Structure.LIST_ITEM,
            Structure.UNORDERED_LIST,
            Structure.UNORDERED_LIST_ITEM]):
        crash(
            law,
            start_index,
            'Use parse_list, parse_list_item, or parse_unordered_list instead'
        )

    '''
    If this doesn't feel intuitive, the best way to understand the algorithm is go through the text
    of the law by hand w/ pen and paper and apply the algorithm as implemented below!
    '''

    initial_start_index = start_index

    end_index = start_index-1
    while end_index < len(law)-1:
        '''
        law[start_index] must be part of the structure we want to parse;
        otherwise the value of start_index passed in was incorrect
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

__MAIN__

-----------------
'''


def print_tree() -> None:
    if ROOT is None:
        print('ROOT=None')
    else:
        print(json.dumps(convert_tree_to_json(ROOT, []), indent=2))


def crash(law: List[str], i: int, error_message: str) -> None:
    print_around(law, i)

    if ROOT is not None:
        with open('./crash.json', 'w') as outfile:
            json.dump(
                convert_tree_to_json(ROOT, []),
                outfile,
                indent=2
            )

    raise Exception(error_message)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('e.g python3 parser.py uu_18_2017')
        exit()

    filename = sys.argv[1]

    law = load_clean_law(filename)

    if len(sys.argv) >= 3 and sys.argv[2] == '--clean':
        exit()

    ROOT = ComplexNode(type=Structure.UNDANG_UNDANG)
    parse_undang_undang(ROOT, law)

    metadata = extract_metadata_from_tree(ROOT)

    if len(sys.argv) >= 3 and sys.argv[2] == '--metadata':
        with open(filename + '_metadata.json', 'w') as outfile:
            json.dump(
                metadata,
                outfile,
                indent=2
            )
        exit()

    assert ROOT is not None

    ketentuan_umum_list = sorted(metadata['ketentuan_umum'].keys(), key=lambda x: len(x), reverse=True)
    content = convert_tree_to_json(ROOT, ketentuan_umum_list)

    with open(filename + '.json', 'w') as outfile:
        json.dump(
            {
                'content': content,
                'metadata': metadata
            },
            outfile,
            indent=2
        )
