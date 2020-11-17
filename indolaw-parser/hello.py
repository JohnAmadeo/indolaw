#from pdfminer.high_level import extract_text, extract_pages
import re

#text = extract_text('tes3.pdf')
#toReplace = {'\n': ' ',
#           '  ': ' ',
#           '   ': ' '}
#
#
#for key, value in toReplace.items():
#    text = text.replace(key, value)
file = open("tes3.txt")
text = file.read()

split_by_bab = re.split('(BAB [MDCLXVI]+)', text)
#print("\n")
for bab in split_by_bab:
    split_by_pasal = re.split('[\n]+[\s]*(Pasal[\s]*[1234567890]*)[\s]*[\n]+', bab)
    print(split_by_pasal)
    # for pasal in split_by_pasal:
    #     z = re.split('()', pasal)
# FROM THIS
#"Irvan's friends are 1. Melissa, 2. John, 3. Evan"

# TO "SOMETHING" LIKE THIS
#{
#  "Irvan's friends are",
#  {
#    1: "Premiumkobebeef",
#    2: "John",
#    3: "Evan"
#  }
#}

# Read the text
# For
# there's a BAB, use that as the first key
#s= "Name1=Value1;Name2=Value2;Name3=Value3"
#dict(item.split("=") for item in s.split(";"))

'''
\nPasal 2\n
Peraturan ini berhubungan dengan Pasal 3 ayat 4


'''