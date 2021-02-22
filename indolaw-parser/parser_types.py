
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
    parent: Union[None, 'ComplexNode'] = None

    def __init__(self, type: Structure, text: str) -> None:
        self.type = type
        self.text = text


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
    parent: Union['ComplexNode', None] = None
    children: List[Union[PrimitiveNode, 'ComplexNode']] = []
    id: str = ''

    def __init__(
        self,
        type: Structure,
        children: List[Union[PrimitiveNode, 'ComplexNode']],
    ) -> None:
        self.type = type

        # set children & parents
        self.children = children
        for child in self.children:
            child.parent = self

        # set id
        if self.type == Structure.BAB:
            bab_number_node = self.children[0]
            assert isinstance(bab_number_node, PrimitiveNode)

            bab_number_roman = bab_number_node.text.split()[1]
            # TODO(johnamadeo): causing a cyclic import
            bab_number_int = self.roman_to_int(bab_number_roman)
            self.id = f'bab-{str(bab_number_int)}'

        elif self.type == Structure.PASAL:
            pasal_number_node = self.children[0]
            assert isinstance(pasal_number_node, PrimitiveNode)

            self.id = f'pasal-{pasal_number_node.text.split()[1]}'

    '''
    This cannot be put in parser_utils because parser_utils also needs to import 
    from parser_types, which would cause a cyclic import problem
    '''
    @staticmethod
    def roman_to_int(roman_numeral: str) -> int:
        """Converts string of a roman numeral to the integer the roman numeral represents
        Logic taken from https://www.w3resource.com/python-exercises/class-exercises/python-class-exercise-2.php

        Args:
            roman_numeral: a string of a roman numeral e.g 'VI', 'LIV'

        Returns:
            int: the integer value of roman_numeral e.g 6, 54

        Examples:
            >>> roman_to_int('IV')
            4
        """
        roman_values = {'I': 1, 'V': 5, 'X': 10,
                        'L': 50, 'C': 100, 'D': 500, 'M': 1000}
        integer = 0
        for i in range(len(roman_numeral)):
            if i > 0 and roman_values[roman_numeral[i]] > roman_values[roman_numeral[i - 1]]:
                integer += roman_values[roman_numeral[i]] - \
                    2 * roman_values[roman_numeral[i - 1]]
            else:
                integer += roman_values[roman_numeral[i]]
        return integer
