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

splitted = text.split("\n")
print(splitted)

law_dict = {}
buffer = ''
index_counter = 0
nest = 1

for content in splitted:
    if content.find("BAB") != -1:
        print("HAHA!")
    elif content.find("Bagian") != -1:
        print("HEHEHE!")
    elif content.find("Pasal") != -1 and content.index("Pasal") <= 1:
        print("HOHO!")

#for char in text:
#    buffer = buffer + char
#    test = re.findall('(BAB [MDCLXVI]+)[\s]*[\n]+', buffer)
#    if test:
#        dict_test[buffer] = ''
#        buffer = ''
#        nest = 1
#    index_counter += 1

#print(dict_test)
    
# {BAB III: JUDUL,
#  BAGIAN: JUDUL BAGIAN,
#  PARAGRAF: Null or PARAGRAF,
#  PASAL+i:
#      {A. : sumthinsumthin,
#       B. : somthinsomthin,
#       C. : soooooooooooomeday,
#       D. :
#          {(1) : nestedvalue,
#           (2) : nestedvalue}
#       E. : somethinnnnng},
#  PASAL 2:
#      continues   
#          }

#re_bab = '(BAB [MDCLXVI]+)'
#re_bagian = '(Bagian Kesatu)'
#re_pasal = '[\n]+[\s]*(Pasal[\s]*[1234567890]*)[\s]*[\n]+'

#split_by_bab = re.split('(BAB [MDCLXVI]+)', text)
#split_by_bagian = re.split('(Bagian Kesatu)', split_by_bab)
#split_by_pasal = re.split('[\n]+[\s]*(Pasal[\s]*[1234567890]*)[\s]*[\n]+', split_by_bagian)

#splitted = re.compile("(%s|%s|%s)" % (re_bab, re_bagian, re_pasal).findall(text))

#print(splitted)
#print("\n")
#dict_by_pasal = {}
#counter = 0
#for bab in split_by_bab:
    # split_by_bab for tes3.txt would be ONE list with TWO values
#    if re.search("(BAB [MDCLXVI]+)", bab):
#        dict_by_pasal[bab] = split_by_bab[counter+1]
#    counter += 1


#for pasal in split_by pasal =
    #return dict_by_pasal
    
#print(split_by_pasal)
#print(dict_by_pasal)  
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