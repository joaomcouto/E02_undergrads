from fuzzywuzzy import fuzz
from fuzzywuzzy import process as fuzzy_process
from nltk.corpus import stopwords

import json

# pattern = "Ivermectina é eficaz contra a covid-19"
# candidates = ['Própria fabricante diz que ivermectina não tem eficácia contra a covid-19','Análise de estudos sobre ivermectina indica eficácia potencial contra Covid-19','Deputado engana ao dizer que ivermectina é eficaz contra covid-19']



# for candidate, score in fuzzy_process.extract(pattern.lower(), list(map(lambda x: x.lower(), candidates)), scorer=fuzz.partial_ratio, limit=1):
#     print(candidate, score)


#file1 = open('DATASET-ALL_true_news.txt', 'r')
#LinesTrue = file1.readlines()

trueNews = []
trueNewsTitles = []
with open('DATASET-ALL_true_news.txt', 'r') as f:
    for line in f:
        #print(line)
        trueNews.append(json.loads(line.strip()))
        trueNewsTitles.append(json.loads(line.strip())['title'])

fakeNews = []
fakeNewsTitles = []
with open('DATASET_MPMG-FakeNews_matched.txt', 'r') as f:
    count = 0
    for line in f:
        count += 1
        fakeNews.append(json.loads(line.strip()))
        fakeNewsTitles.append(json.loads(line.strip())['title'])

def filter_stopwords_from_list(aList):
    ret = [a.lower() for a in aList if a.lower() not in stopwords.words('portuguese')]
    return ret

#candidatesRaw = list(trueNewsTitles)
#candidates = [a.split() for a in candidatesRaw]
candidates = [" ".join(filter_stopwords_from_list(a.split())) for a in trueNewsTitles]
#print(candidates[13974])
#print(trueNewsTitles[13974])
#print(candidates.index("pandemia"))
#print(trueNewsTitles[candidates.index("pandemia")])
#print(trueNews[candidates.index("pandemia")])
#print(candidatesRaw[13974])
#print(len(candidates))

for patternRaw in fakeNewsTitles:
    pattern = patternRaw.split()
    pattern = [a.lower() for a in pattern if a.lower() not in stopwords.words('portuguese')]
    pattern = " ".join(pattern)

    print(pattern + ':' )
    bestMatchIndexes = []

    print("Ratio:")
    for candidate, score in fuzzy_process.extract(pattern.lower(), list(map(lambda x: x.lower(), candidates)), scorer=fuzz.ratio, limit=5):
        bestMatchIndexes.append(candidates.index(candidate))

        temp = []
        temp.append(candidates.index(candidate))
        tempPatternMatches = [trueNewsTitles[i] for i in temp]
        for a in tempPatternMatches:
            print("\t" + a )

    print("Partial ratio:")
    for candidate, score in fuzzy_process.extract(pattern.lower(), list(map(lambda x: x.lower(), candidates)), scorer=fuzz.partial_ratio, limit=5):
        bestMatchIndexes.append(candidates.index(candidate))

        temp = []
        temp.append(candidates.index(candidate))
        tempPatternMatches = [trueNewsTitles[i] for i in temp]
        for a in tempPatternMatches:
            print("\t" + a )

    print("Token sort:")
    for candidate, score in fuzzy_process.extract(pattern.lower(), list(map(lambda x: x.lower(), candidates)), scorer=fuzz.token_sort_ratio, limit=5):
        bestMatchIndexes.append(candidates.index(candidate))

        temp = []
        temp.append(candidates.index(candidate))
        tempPatternMatches = [trueNewsTitles[i] for i in temp]
        for a in tempPatternMatches:
            print("\t" + a )

    print("Token set:")
    for candidate, score in fuzzy_process.extract(pattern.lower(), list(map(lambda x: x.lower(), candidates)), scorer=fuzz.token_set_ratio, limit=5):
        bestMatchIndexes.append(candidates.index(candidate))

        temp = []
        temp.append(candidates.index(candidate))
        tempPatternMatches = [trueNewsTitles[i] for i in temp]
        for a in tempPatternMatches:
            print("\t" + a )

    bestMatchIndexes = list(set(bestMatchIndexes))
    patternMatches = [trueNewsTitles[i] for i in bestMatchIndexes]

    # for a in patternMatches:
    #     print("\t" + a + "\n")
    
    # #print("\t" + candidate, score)
    # print("\n\n")

#print(fakeNewsTitles)
