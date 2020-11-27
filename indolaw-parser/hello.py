#from pdfminer.high_level import extract_text, extract_pages
#import re
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


def detect_hierarchy(hierarchy):
    count = 0
    if hierarchy["bagian"]:
        count += 1
    if hierarchy["paragraf"]:
        count += 1
    return count


def detect_nest_hierarchy(metadata_dict):
    count = 0
    if metadata_dict["Nest 1"]:
        count += 1
    if metadata_dict["Nest 2"]:
        count += 1
    return count


def parse_law(law):
    law = list(filterfalse(ignore_line, law))

    law_dict = {}
    buffer = ''
    current_hierarchy = {"bab": "",
                         "bagian": "",
                         "paragraf": "",
                         "pasal": "",
                         "type": 0,
                         "level": 0,
                         "nest 1": "",
                         "nest 2": ""}

    last_line = len(law) - 1

    # please for godforsaken sake, change this into
    # something recursive :')

    for i, line in enumerate(law):
        # print(i)
        temp = {}
        hierarchy = 0
        if "BAB" in line and i < last_line:
            law_dict[line] = {
                'title': law[i+1],
                'contents': {},
            }
            current_hierarchy["bab"] = line
            # TODO(john): Is this meant for resetting the current bagian & paragraf we're currently at?
            # If so, do we need to "hard reset" contents of all hierarchies deeper than bab?
            current_hierarchy['bagian'] = ""
            current_hierarchy['paragraf'] = ""
        elif "Bagian" in line and i < last_line:
            current_bab = current_hierarchy['bab']
            law_dict[current_bab]['contents'][line] = {
                'title': law[i+1],
                'contents': {},
            }
            current_hierarchy['bagian'] = line
        elif "Paragraf" in line and i < last_line:
            current_bab = current_hierarchy['bab']
            bagian_dict = law_dict[current_bab]['contents']
            current_bagian = current_hierarchy['bagian']
            paragraf_dict = bagian_dict[current_bagian]['contents']
            paragraf_dict[line] = {
                'title': law[i+1],
                'contents': {},
            }

            current_hierarchy["paragraf"] = line
        # TODO(johnamadeo): this doesn't work for nested pasals (see omnibus_law_pg_12_13.pdf)
        elif ("Pasal" in line and line.rstrip().index("Pasal") == 0) and i < last_line:
            temp["Isi Pasal"] = {}
            if detect_list_type(law[i+1]) == ListType.INVALID:
                temp["Teks"] = law[i+1]

            # check if pasal is attached to a bab, bagian, or paragraf
            hierarchy = detect_hierarchy(current_hierarchy)
            current_bab = current_hierarchy['bab']
            if hierarchy == 0:
                law_dict[current_bab]['contents'][line] = temp
            else:
                current_bagian = current_hierarchy['bagian']
                bagian_dict = law_dict[current_bab]['contents'][current_bagian]

                if hierarchy == 1:
                    bagian_dict['contents'][line] = temp
                elif hierarchy == 2:
                    current_paragraf = current_hierarchy['paragraf']
                    paragraf_dict = bagian_dict['contents'][current_paragraf]

                    paragraf_dict['contents'][line] = temp

            current_hierarchy["pasal"] = line
            current_hierarchy["nest 1"] = ""

        # elif detect_list_type(line) > 0:
        #     key = line[0:3]
        #     hierarchy = detect_hierarchy(hie)
        #     nest_type = detect_list_type(line)
        #     temp[key] = line[3:-1]
        #     # If it's the first nest level of the pasal
        #     if hie["Nest 1"] == "":
        #         #temp[key] = line[3:-1]
        #         hie["Type"] = nest_type
        #         hie["Nest 1"] = key

        #     # Else if it's not the same type of starting letters
        #     elif hie["Type"] != nest_type:
        #         # Check if the currently iterated type is the same
        #         # with higher level type
        #         if detect_list_type(hie["Nest 1"]) == nest_type:
        #             #temp[key] = line[3:-1]
        #             hie["Nest 1"] = key
        #             hie["Level"] = 0
        #         else:
        #             hie["Nest 2"] = key
        #             hie["Level"] = 1
        #         hie["Type"] == nest_type

        #     # If type is the same
        #     # elif hie["Type"] == nest_type:
        #     #    if hie["Level"] == 0:
        #     #        temp[key] = line[3:-1]
        #     #    if hie["Level"] == 1:
        #     #        temp[key] = line[3:-1]
        #     if hierarchy == 0 and hie["Level"] == 1:
        #         law_dict[hie["BAB"]]["Isi Bab"][hie["Pasal"]
        #                                         ]["Isi Pasal"][hie["Nest 1"]] = temp
        #     elif hierarchy == 0 and hie["Level"] == 0:
        #         law_dict[hie["BAB"]]["Isi Bab"][hie["Pasal"]
        #                                         ]["Isi Pasal"][key] = line[3:-1]
        #     elif hierarchy == 1 and hie["Level"] == 1:
        #         law_dict[hie["BAB"]]["Isi Bab"][hie["Bagian"]
        #                                         ]["Isi Bagian"][hie["Pasal"]]["Isi Pasal"][hie["Nest 1"]] = temp
        #     elif hierarchy == 1 and hie["Level"] == 0:
        #         law_dict[hie["BAB"]]["Isi Bab"][hie["Bagian"]
        #                                         ]["Isi Bagian"][hie["Pasal"]]["Isi Pasal"][key] = line[3:-1]
        #     elif hierarchy == 2 and hie["Level"] == 1:
        #         law_dict[hie["BAB"]]["Isi Bab"][hie["Bagian"]]["Isi Bagian"][hie["Paragraf"]
        #                                                                      ]["Isi Paragraf"][hie["Pasal"]]["Isi Pasal"][hie["Nest 1"]] = temp
        #     elif hierarchy == 2 and hie["Level"] == 0:
        #         law_dict[hie["BAB"]]["Isi Bab"][hie["Bagian"]]["Isi Bagian"][hie["Paragraf"]
        #                                                                      ]["Isi Paragraf"][hie["Pasal"]]["Isi Pasal"][key] = line[3:-1]


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

# for char in text:
#    buffer = buffer + char
#    test = re.findall('(BAB [MDCLXVI]+)[\s]*[\n]+', buffer)
#    if test:
#        dict_test[buffer] = ''
#        buffer = ''
#        nest = 1
#    index_counter += 1

# print(dict_test)

# {BAB III: {
#        JUDUL BAB: Judul,
#        ISI BAB: {
#       BAGIAN: Null or JUDUL BAGIAN,
#       PARAGRAF: Null or PARAGRAF,
#       PASAL 1: Null or text,
#       isi pasal:
#           {A. : sumthinsumthin,
#            B. : somthinsomthin,
#            C. : soooooooooooomeday,
#            D. :
#               {(1) : nestedvalue,
#                (2) : nestedvalue}
#            E. : somethinnnnng},
#       PASAL 2:
#           continues
#          }}

#re_bab = '(BAB [MDCLXVI]+)'
#re_bagian = '(Bagian Kesatu)'
#re_pasal = '[\n]+[\s]*(Pasal[\s]*[1234567890]*)[\s]*[\n]+'

#split_by_bab = re.split('(BAB [MDCLXVI]+)', text)
#split_by_bagian = re.split('(Bagian Kesatu)', split_by_bab)
#split_by_pasal = re.split('[\n]+[\s]*(Pasal[\s]*[1234567890]*)[\s]*[\n]+', split_by_bagian)

#law = re.compile("(%s|%s|%s)" % (re_bab, re_bagian, re_pasal).findall(text))

# print(law)
# print("\n")
#dict_by_pasal = {}
#counter = 0
# for bab in split_by_bab:
# split_by_bab for tes3.txt would be ONE list with TWO values
#    if re.search("(BAB [MDCLXVI]+)", bab):
#        dict_by_pasal[bab] = split_by_bab[counter+1]
#    counter += 1


# for pasal in split_by pasal =
# return dict_by_pasal

# print(split_by_pasal)
# print(dict_by_pasal)
# for pasal in split_by_pasal:
#     z = re.split('()', pasal)


# FROM THIS

#"Irvan's friends are 1. Melissa, 2. John, 3. Evan"

# TO "SOMETHING" LIKE THIS
# {
#  "Irvan's friends are",
#  {
#    1: "Premiumkobebeef",
#    2: "John",
#    3: "Evan"
#  }
# }

# Read the text
# For
# there's a BAB, use that as the first key
#s= "Name1=Value1;Name2=Value2;Name3=Value3"
#dict(item.split("=") for item in s.split(";"))
