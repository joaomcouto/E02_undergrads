# import env
# import os
# import unidecode
# #LOG_FILENAME = os.getenv('PROJECT_DIR') + "/" + 'G1/LOG/' + "historica" + '.log'
# LOG_FILENAME = os.getenv('PROJECT_DIR') + "/" + 'UOL/URL/' + "UOL_coronavirus_882_loads" + '.txt'
# undesirables = ['/videos','/colunas','/album','/reportagens-especiais', '/amp-stories', 'band.uol','stories','faq']
# with open(LOG_FILENAME) as f:
#     for line in f:
#         #if("ERROR" in line):
#         #if("/post" in line):
#         if("/2021" not in line and '/2020' not in line):
#             a = [und for und in undesirables if und not in line]
#             #print(a)
#             #if('blog' not in line):
#             #if("2021" in line):
#             #if()
#             if(len(a) == len(undesirables)):
#                 print(line)
#             #print(line.split('.com/')[1].split('/noticia')[0].split('/'))
#             #print("\n")


import unicodedata

def strip_accents(text):

    try:
        text = unicode(text, 'utf-8')
    except NameError: # unicode is a default on python 3 
        pass

    text = unicodedata.normalize('NFD', text)\
           .encode('ascii', 'ignore')\
           .decode("utf-8")

    return str(text)

s = strip_accents('àéêöhello')

print (s)