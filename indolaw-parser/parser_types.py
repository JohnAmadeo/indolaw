
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

Primitive = TypedDict('Primitive', {'type': str, 'text': str})

# Python has trouble with recursive types e.g in this case we want to use the Complex type in the definition
# of the Complex type itself (i.e the classic CS tree data structure)
# https://www.python.org/dev/peps/pep-0484/#the-problem-of-forward-declarations
Complex = TypedDict('Complex', {
                    'type': str, 'id': Optional[str], 'children': List[Union[Primitive, 'Complex']]})  # type: ignore
