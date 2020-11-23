#from pdfminer.high_level import extract_text, extract_pages
#import re
import json

#text = extract_text('tes3.pdf')
# toReplace = {'\n': ' ',
#           '  ': ' ',
#           '   ': ' '}
#
#
# for key, value in toReplace.items():
#    text = text.replace(key, value)
file = open("tes.txt")
text = file.read()

splitted = text.split("\n")

law_dict = {}
buffer = ''
hie = {"BAB": "",
       "Bagian": "",
       "Paragraf": "",
       "Pasal": "",
       "Type": 0,
       "Level": 0,
       "Nest 1": "",
       "Nest 2": ""}


def detect_nest_type(content):
    if content[0] == "(" and content[2] == ")":
        return 1
    elif (content[1] == '.' or content[2] == '.') and content[0].isdigit():
        return 2
    elif content[1] == '.' and content[0].islower():
        return 3
    else:
        return 0


def detect_hierarchy(metadata_dict):
    count = 0
    if metadata_dict["Bagian"]:
        count += 1
    if metadata_dict["Paragraf"]:
        count += 1
    return count


def detect_nest_hierarchy(metadata_dict):
    count = 0
    if metadata_dict["Nest 1"]:
        count += 1
    if metadata_dict["Nest 2"]:
        count += 1
    return count


eol = len(splitted) - 1


# please for godforsaken sake, change this into
# something recursive :')

for i, content in enumerate(splitted):
    temp = {}
    hierarchy = 0
    if content.find(". . .") != -1:
        continue
    if content.find("BAB") != -1 and i < eol:
        temp["Judul Bab"] = splitted[i+1]
        temp["Isi Bab"] = {}
        law_dict[content] = temp
        hie["BAB"] = content
        hie["Bagian"] = ""
        hie["Paragraf"] = ""
    elif content.find("Bagian") != -1 and i < eol:
        temp["Judul Bagian"] = splitted[i+1]
        temp["Isi Bagian"] = {}
        law_dict[hie["BAB"]]["Isi Bab"][content] = temp
        hie["Bagian"] = content
    elif content.find("Paragraf") != -1 and i < eol:
        temp["Judul Paragraf"] = splitted[i+1]
        temp["Isi Paragraf"] = {}
        law_dict[hie["BAB"]]["Isi Bab"][hie["Bagian"]
                                        ]["Isi Bagian"][content] = temp
        hie["Paragraf"] = content
    elif (content.find("Pasal") != -1 and content.index("Pasal") <= 1) and i < eol:
        if detect_nest_type(splitted[i+1]):
            temp["Isi Pasal"] = {}
        else:
            temp["Teks"] = splitted[i+1]
            temp["Isi Pasal"] = {}
        hierarchy = detect_hierarchy(hie)
        if hierarchy == 0:
            law_dict[hie["BAB"]]["Isi Bab"][content] = temp
        elif hierarchy == 1:
            law_dict[hie["BAB"]]["Isi Bab"][hie["Bagian"]
                                            ]["Isi Bagian"][content] = temp
        else:
            law_dict[hie["BAB"]]["Isi Bab"][hie["Bagian"]
                                            ]["Isi Bagian"][hie["Paragraf"]]["Isi Paragraf"][content] = temp
        hie["Pasal"] = content
        hie["Nest 1"] = ""
    elif detect_nest_type(content) > 0:
        key = content[0:3]
        hierarchy = detect_hierarchy(hie)
        nest_type = detect_nest_type(content)
        temp[key] = content[3:-1]
        # If it's the first nest level of the pasal
        if hie["Nest 1"] == "":
            #temp[key] = content[3:-1]
            hie["Type"] = nest_type
            hie["Nest 1"] = key

        # Else if it's not the same type of starting letters
        elif hie["Type"] != nest_type:
            # Check if the currently iterated type is the same
            # with higher level type
            if detect_nest_type(hie["Nest 1"]) == nest_type:
                #temp[key] = content[3:-1]
                hie["Nest 1"] = key
                hie["Level"] = 0
            else:
                hie["Nest 2"] = key
                hie["Level"] = 1
            hie["Type"] == nest_type

        # If type is the same
        # elif hie["Type"] == nest_type:
        #    if hie["Level"] == 0:
        #        temp[key] = content[3:-1]
        #    if hie["Level"] == 1:
        #        temp[key] = content[3:-1]
        if hierarchy == 0 and hie["Level"] == 1:
            law_dict[hie["BAB"]]["Isi Bab"][hie["Pasal"]
                                            ]["Isi Pasal"][hie["Nest 1"]] = temp
        elif hierarchy == 0 and hie["Level"] == 0:
            law_dict[hie["BAB"]]["Isi Bab"][hie["Pasal"]
                                            ]["Isi Pasal"][key] = content[3:-1]
        elif hierarchy == 1 and hie["Level"] == 1:
            law_dict[hie["BAB"]]["Isi Bab"][hie["Bagian"]
                                            ]["Isi Bagian"][hie["Pasal"]]["Isi Pasal"][hie["Nest 1"]] = temp
        elif hierarchy == 1 and hie["Level"] == 0:
            law_dict[hie["BAB"]]["Isi Bab"][hie["Bagian"]
                                            ]["Isi Bagian"][hie["Pasal"]]["Isi Pasal"][key] = content[3:-1]
        elif hierarchy == 2 and hie["Level"] == 1:
            law_dict[hie["BAB"]]["Isi Bab"][hie["Bagian"]]["Isi Bagian"][hie["Paragraf"]
                                                                         ]["Isi Paragraf"][hie["Pasal"]]["Isi Pasal"][hie["Nest 1"]] = temp
        elif hierarchy == 2 and hie["Level"] == 0:
            law_dict[hie["BAB"]]["Isi Bab"][hie["Bagian"]]["Isi Bagian"][hie["Paragraf"]
                                                                         ]["Isi Paragraf"][hie["Pasal"]]["Isi Pasal"][key] = content[3:-1]

with open("example.json", "w") as outfile:
    json.dump(law_dict, outfile)

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

#splitted = re.compile("(%s|%s|%s)" % (re_bab, re_bagian, re_pasal).findall(text))

# print(splitted)
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

'''
\nPasal 2\n
Peraturan ini berhubungan dengan Pasal 3 ayat 4


'''
