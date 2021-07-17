
from enum import Enum
from typing import Any, Dict, List, Optional, Union
from typing_extensions import TypedDict


class Structure(Enum):
    # END = "End"
    # SKIP = "Skip"
    UNDANG_UNDANG = "UNDANG_UNDANG"
    OPENING = "OPENING"
    UU_TITLE = "UU_TITLE"
    UU_TITLE_YEAR_AND_NUMBER = "UU_TITLE_YEAR_AND_NUMBER"
    UU_TITLE_TOPIC = "UU_TITLE_TOPIC"
    PREFACE = "PREFACE"
    CONSIDERATIONS = "CONSIDERATIONS"
    PRINCIPLES = "PRINCIPLES"
    AGREEMENT = "AGREEMENT"
    BAB = "BAB"
    BAB_NUMBER = "BAB_NUMBER"
    BAB_TITLE = "BAB_TITLE"
    PASAL = "PASAL"
    PASAL_NUMBER = "PASAL_NUMBER"
    PERUBAHAN_SECTION = "PERUBAHAN_SECTION"
    PERUBAHAN_PASAL = "PERUBAHAN_PASAL"
    PERUBAHAN_BAB = "PERUBAHAN_BAB"
    PERUBAHAN_BAGIAN = "PERUBAHAN_BAGIAN"
    PENJELASAN_PERUBAHAN_SECTION = "PENJELASAN_PERUBAHAN_SECTION"
    PENJELASAN_PERUBAHAN_PASAL = "PENJELASAN_PERUBAHAN_PASAL"
    PENJELASAN_PERUBAHAN_BAB = "PENJELASAN_PERUBAHAN_BAB"
    PENJELASAN_PERUBAHAN_BAGIAN = "PENJELASAN_PERUBAHAN_BAGIAN"
    BAGIAN = "BAGIAN"
    BAGIAN_TITLE = "BAGIAN_TITLE"
    BAGIAN_NUMBER = "BAGIAN_NUMBER"
    PARAGRAF = "PARAGRAF"
    PARAGRAF_TITLE = "PARAGRAF_TITLE"
    PARAGRAF_NUMBER = "PARAGRAF_NUMBER"
    CLOSING = "CLOSING"
    LEMBARAN_NUMBER = "LEMBARAN_NUMBER"
    PENJELASAN = "PENJELASAN"
    PENJELASAN_TITLE = "PENJELASAN_TITLE"
    PENJELASAN_UMUM = "PENJELASAN_UMUM"
    PENJELASAN_UMUM_TITLE = "PENJELASAN_UMUM_TITLE"
    PENJELASAN_PASAL_DEMI_PASAL = "PENJELASAN_PASAL_DEMI_PASAL"
    PENJELASAN_PASAL_DEMI_PASAL_TITLE = "PENJELASAN_PASAL_DEMI_PASAL_TITLE"
    PENJELASAN_PASAL = "PENJELASAN_PASAL"
    PENJELASAN_LIST_ITEM = "PENJELASAN_LIST_ITEM"
    UNORDERED_LIST = "UNORDERED_LIST"
    UNORDERED_LIST_ITEM = "UNORDERED_LIST_ITEM"
    UNORDERED_LIST_INDEX = "UNORDERED_LIST_INDEX"
    PLAINTEXT = "PLAINTEXT"
    LIST = "LIST"
    LIST_ITEM = "LIST_ITEM"
    LIST_INDEX = "LIST_INDEX"
    NUMBER_WITH_BRACKETS = "NUMBER_WITH_BRACKETS"
    NUMBER_WITH_RIGHT_BRACKET = "NUMBER_WITH_RIGHT_BRACKET"
    NUMBER_WITH_DOT = "NUMBER_WITH_DOT"
    LETTER_WITH_DOT = "LETTER_WITH_DOT"
    LETTER_WITH_BRACKETS = "LETTER_WITH_BRACKETS"
    LETTER_WITH_RIGHT_BRACKET = "LETTER_WITH_RIGHT_BRACKET"
    PENJELASAN_HURUF = "PENJELASAN_HURUF"
    PENJELASAN_AYAT = "PENJELASAN_AYAT"
    PENJELASAN_ANGKA = "PENJELASAN_ANGKA"
    PENJELASAN_ANGKA_WITH_RIGHT_BRACKET = "PENJELASAN_ANGKA_WITH_RIGHT_BRACKET"
    FORMATTED_MATH_ROW = "FORMATTED_MATH_ROW"


TEXT_BLOCK_STRUCTURES = [
    Structure.FORMATTED_MATH_ROW,
    Structure.PLAINTEXT,
    Structure.LIST,
    Structure.UNORDERED_LIST,
]

'''
The list of types that a Primitive structure can be
'''
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


ListIndexDefinition = Dict[str, Union[str, bool]]


class PrimitiveNode:
    '''
    A primitive node is a node:
    a) which doesn't have children nodes
    b) whose content is a string

    If we look at the tree of nodes that define a law, all
    the leaf nodes of the law tree are primitive nodes, and all primitive nodes can
    only be found as leafs.

    e.g {
        'type': 'BAB_NUMBER',
        'text': 'BAB XIV'
    }
    '''

    def __init__(
        self,
        type: Structure,
        text: str,
        formatting: Dict[str, Any] = {},
    ) -> None:
        self.type = type
        self.text = text
        self.parent: Union[None, 'ComplexNode'] = None
        self.formatting: Dict[str, Any] = formatting
        self.id = ''


class ComplexNode:
    """
    A complex node is a node whose content is a list of other nodes, as opposed
    to a string.

    If we look at the tree of nodes that define a law, all the non-leaf nodes of the law tree
    are complex nodes.

    e.g {
        'type': 'BAB',
        'id': 'bab-3',
        'children': [
            { type: 'BAB_NUMBER', ... },
            { type: 'BAB_TITLE', ... },
            { type: 'PASAL', ... },
        ]
    }
    """

    def __init__(
        self,
        type: Structure,
    ) -> None:
        self.type = type
        self.children: List[Union[PrimitiveNode, 'ComplexNode']] = []
        self.parent: Union[None, 'ComplexNode'] = None
        self.id = ''

    def add_child(self, child: Union[PrimitiveNode, 'ComplexNode']):
        self.children.append(child)
        child.parent = self


class PlaintextInListItemScenario(Enum):
    SIBLING_OF_LIST = "SIBLING_OF_LIST"
    CHILD_OF_LIST_ITEM = "CHILD_OF_LIST_ITEM"
    FORMATTED_MATH_ROW_CHILD_OF_LIST_ITEM = "FORMATTED_MATH_CHILD_OF_LIST_ITEM"
    EMBEDDED_LAW_SNIPPET = "EMBEDDED_LAW_SNIPPET"
