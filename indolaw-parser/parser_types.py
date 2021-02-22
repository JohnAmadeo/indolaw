
from enum import Enum
from typing import List, Optional, Union
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

LIST_INDEX_STRUCTURES = [Structure.NUMBER_WITH_BRACKETS,
                         Structure.NUMBER_WITH_DOT, Structure.LETTER_WITH_DOT]


class PrimitiveNode:
    '''
    A primitive node is a node whose content is a string, as opposed to a
    list of other nodes.

    If we look at the tree of nodes that define a law, all
    the leaf nodes of the law tree are primitive nodes, and all primitive nodes can
    only be found as leafs.

    e.g {
        'type': 'BAB_NUMBER',
        'text': 'BAB XIV'
    }
    '''

    def __init__(self, type: Structure, text: str) -> None:
        self.type = type
        self.text = text
        self.parent: Union[None, 'ComplexNode'] = None
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
