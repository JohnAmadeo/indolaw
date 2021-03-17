'''
-----------------

DEPRECATED - DON'T USE (FOR NOW)

-----------------
'''


import json
import re
import sys
from enum import Enum
from itertools import filterfalse
from os import system, name
from colorama import init
from termcolor import colored

'''
Use Colorama to make Termcolor work on Windows too
See https://pypi.org/project/colorama/ for more
'''
init()


class Structure(Enum):
    END = "End"
    SKIP = "Skip"

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

    TEXT_BLOCK = "Text Block"
    PLAINTEXT = "Plaintext"

    LIST = "List"
    LIST_ITEM = "List Item"
    LIST_INDEX = "List Index"
    NUMBER_IN_BRACKETS = "Number in Brackets"
    NUMBER_WITH_DOT = "Number with Dot"
    LETTER_WITH_DOT = "Letter with Dot"


def ignore_line(line):
    if ". . ." in line:
        return True
    # page number
    elif re.match('- [0-9]+ -', line.rstrip()) != None:
        return True
    else:
        return False


def get_text_block_structures():
    return [Structure.PLAINTEXT, Structure.LIST, Structure.PASAL]


'''
-----------------

UI

-----------------
'''


def get_line_with_context(law, current_line, current_line_index, parent_structure):
    previous_line = ""
    next_line = ""

    if current_line_index > 0:
        previous_line = previous_line = law[current_line_index-1]
    if current_line_index < len(law)-1:
        next_line = law[current_line_index+1]

    line_with_context = """
---------------------------------
{previous_line}

>>> {current_line}

{next_line}
---------------------------------

Parent Structure: {parent_structure}
    """.format(
        previous_line=previous_line,
        current_line=current_line,
        next_line=next_line,
        parent_structure=colored(parent_structure.value, 'red'),
    )

    return line_with_context


def get_structure_options(options):
    colors = ['green', 'yellow', 'blue', 'magenta', 'cyan']
    option_strings = []
    for i, option in enumerate(options):
        option_string = "{num}. {option}".format(num=i, option=option.value)
        option_string = colored(option_string, colors[i % len(colors)])
        option_strings.append(option_string)

    return ", ".join(option_strings) + "\n"


def clear():
    # i.e Windows
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')


'''
-----------------

COMPLEX

-----------------
'''


def parse_undang_undang(law):
    # TODO: safety checks
    law = list(filterfalse(ignore_line, law))
    options = [Structure.BAB]
    return parse_complex_structure(options, law, 0, Structure.UNDANG_UNDANG)


def parse_bab(law, start_index):
    options = [Structure.BAB_NUMBER, Structure.BAB_TITLE,
               Structure.PASAL, Structure.BAGIAN]
    return parse_complex_structure(options, law, start_index, Structure.BAB)


def parse_pasal(law, start_index):
    options = [Structure.PASAL_NUMBER] + get_text_block_structures()
    return parse_complex_structure(options, law, start_index, Structure.PASAL)


def parse_text_block(law, start_index):
    options = [Structure.PLAINTEXT, Structure.LIST, Structure.PASAL]
    return parse_complex_structure(options, law, start_index, Structure.TEXT_BLOCK)


def parse_list(law, start_index):
    options = [Structure.LIST_ITEM]
    return parse_complex_structure(options, law, start_index, Structure.LIST)


def parse_bagian(law, start_index):
    options = [Structure.BAGIAN_NUMBER, Structure.BAGIAN_TITLE,
               Structure.PASAL, Structure.PARAGRAF]
    return parse_complex_structure(options, law, start_index, Structure.BAGIAN)


def parse_paragraf(law, start_index):
    options = [Structure.PARAGRAF_NUMBER,
               Structure.PARAGRAF_TITLE, Structure.PASAL]
    return parse_complex_structure(options, law, start_index, Structure.PARAGRAF)


def parse_list_item(law, start_index):
    parsed_list_index, _ = parse_list_index(law, start_index)
    parsed_list_item = [parsed_list_index]

    options = get_text_block_structures()

    parsed_structure, end_index = parse_complex_structure(
        options, law, start_index, Structure.LIST_ITEM)
    parsed_list_item.extend(parsed_structure)

    return parsed_list_item, end_index


def parse_complex_structure(options, law, start_index, parent_structure):
    options = options + [Structure.END, Structure.SKIP]
    parsed_structure = []

    end_index = start_index-1
    while end_index < len(law)-1:
        line_with_context = get_line_with_context(
            law, law[start_index], start_index, parent_structure)
        print(line_with_context)

        # TODO make response typed
        user_input = input(get_structure_options(options))
        clear()

        structure = options[int(user_input)]
        if structure == Structure.END:
            return parsed_structure, end_index
        if structure == Structure.SKIP:
            start_index += 1
            continue

        parsed_sub_structure, end_index = parse_structure(
            structure, law, start_index)
        start_index = end_index + 1

        parsed_structure.append(parsed_sub_structure)

    return parsed_structure, end_index


'''
-----------------

PRIMITIVES

-----------------
'''


def parse_bab_number(law, start_index):
    return parse_primitive(Structure.BAB_NUMBER, law, start_index)


def parse_bab_title(law, start_index):
    return parse_primitive(Structure.BAB_TITLE, law, start_index)


def parse_bagian_title(law, start_index):
    return parse_primitive(Structure.BAGIAN_TITLE, law, start_index)


def parse_bagian_number(law, start_index):
    return parse_primitive(Structure.BAGIAN_NUMBER, law, start_index)


def parse_paragraf_title(law, start_index):
    return parse_primitive(Structure.PARAGRAF_TITLE, law, start_index)


def parse_paragraf_number(law, start_index):
    return parse_primitive(Structure.PARAGRAF_NUMBER, law, start_index)


def parse_pasal_number(law, start_index):
    return parse_primitive(Structure.PASAL_NUMBER, law, start_index)


def parse_plaintext(law, start_index):
    return parse_primitive(Structure.PLAINTEXT, law, start_index)


def parse_primitive(structure, law, start_index):
    return {
        'type': structure.value,
        'plaintext': law[start_index].rstrip()
    }, start_index


def parse_list_index(law, start_index):
    options = [Structure.LETTER_WITH_DOT,
               Structure.NUMBER_IN_BRACKETS, Structure.NUMBER_WITH_DOT]

    line_with_context = get_line_with_context(
        law, law[start_index], start_index, Structure.LIST_INDEX)
    print(line_with_context)

    # TODO make response typed
    user_input = input(get_structure_options(options))
    clear()
    structure = options[int(user_input)]

    return {
        'type': structure.value,
        'list_index': law[start_index].split(' ')[0],
    }, start_index


'''
-----------------

STRUCTURE CONTROL

-----------------
'''


def parse_structure(structure, law, start_index):
    if structure == Structure.BAB:
        return parse_bab(law, start_index)
    elif structure == Structure.BAB_NUMBER:
        return parse_bab_number(law, start_index)
    elif structure == Structure.BAB_TITLE:
        return parse_bab_title(law, start_index)
    elif structure == Structure.PASAL:
        return parse_pasal(law, start_index)
    elif structure == Structure.PASAL_NUMBER:
        return parse_pasal_number(law, start_index)
    elif structure == Structure.BAGIAN:
        return parse_bagian(law, start_index)
    elif structure == Structure.BAGIAN_NUMBER:
        return parse_bagian_number(law, start_index)
    elif structure == Structure.BAGIAN_TITLE:
        return parse_bagian_title(law, start_index)
    elif structure == Structure.PARAGRAF:
        return parse_paragraf(law, start_index)
    elif structure == Structure.PARAGRAF_NUMBER:
        return parse_paragraf_number(law, start_index)
    elif structure == Structure.PARAGRAF_TITLE:
        return parse_paragraf_title(law, start_index)
    elif structure == Structure.TEXT_BLOCK:
        return parse_text_block(law, start_index)
    elif structure == Structure.PLAINTEXT:
        return parse_plaintext(law, start_index)
    elif structure == Structure.LIST:
        return parse_list(law, start_index)
    elif structure == Structure.LIST_ITEM:
        return parse_list_item(law, start_index)
    elif structure == Structure.LIST_INDEX:
        return parse_list_index(law, start_index)
    else:
        raise Exception("No function can parse " + structure)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('e.g python3 law_parser.py omnibus_law_pg_3_4')
        exit()

    filename = sys.argv[1]
    file = open(
        filename + '.txt',
        mode='r',
        encoding='utf-8-sig')
    law = file.read().split("\n")

    parsed_law, _ = parse_undang_undang(law)
    print(parsed_law)

    with open(filename + '.json', 'w') as outfile:
        json.dump(parsed_law, outfile)
