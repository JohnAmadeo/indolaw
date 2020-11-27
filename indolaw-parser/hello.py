import json
from enum import Enum
import sys
import re
from itertools import filterfalse


class ListType(Enum):
    INVALID = 0
    NUMBER_IN_BRACKETS = 1
    NUMBER_WITH_DOT = 2
    LETTER_WITH_DOT = 3


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
    # LIST = "List"
    # LIST_ITEM = "List Item"
    # LIST_INDEX = "List Index"
    # NUMBER_IN_BRACKETS = "Number in Brackets"
    # NUMBER_WITH_DOT = "Number with Dot"
    # LETTER_WITH_DOT = "Letter with Dot"
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
        return ListType.NUMBER_IN_BRACKETS
    # e.g 5.
    # TODO(johnamadeo): Use regex instead - this doesn't work for 112.
    elif (line[1] == '.' or line[2] == '.') and line[0].isdigit():
        return ListType.NUMBER_WITH_DOT
    # e.g c.
    elif line[1] == '.' and line[0].islower():
        return ListType.LETTER_WITH_DOT
    else:
        return ListType.INVALID






    law = list(filterfalse(ignore_line, law))



if __name__ == "__main__":
    filename = "tes.txt"
    if len(sys.argv) > 2:
        filename = sys.argv[1]

    file = open(
        filename + '.txt',
        mode='r',
        encoding='utf-8-sig')
    law = file.read().split("\n")

    structured_law = parse_law(law)

    with open(filename + '.json', 'w') as outfile:
        json.dump(structured_law, outfile)

