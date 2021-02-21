
from enum import Enum
from typing import List, Optional, Union
from typing_extensions import TypedDict


'''
A Primitive structure is a structure whose content is a string, as opposed to a
list of other structures. 

If we look at the tree of structures that define a law, all
the leaf nodes of the law tree are Primitive structures, and all Primitive structures can
only be found as leafs.

e.g {
    'type': 'BAB_NUMBER',
    'text': 'BAB XIV'
}
'''
Primitive = TypedDict('Primitive', {'type': str, 'text': str})

'''
A Complex structure is a structure whose content is a list of other structures, as opposed
to a string.

If we look at the tree of structures that define a law, all the non-leaf nodes of the law tree 
are Complex structures.

e.g {
    'type': 'BAB',
    'id': 'bab-3',
    'children': [
        { type: 'BAB_NUMBER', ... },
        { type: 'BAB_TITLE', ... },
        { type: 'PASAL', ... },
    ]
}
'''
Complex = TypedDict(
    'Complex', {
        'type': str,
        # unique ID that we leverage to create HTML links to specific sections
        # e.g hukumjelas.com/uu/keimigrasian#pasal-4
        'id': Optional[str],
        # Python has trouble with recursive types (i.e the classic CS tree data structure)
        # https://www.python.org/dev/peps/pep-0484/#the-problem-of-forward-declarations
        'children': List[Union[Primitive, 'Complex']]  # type: ignore
    }
)


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
