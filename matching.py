from fuzzywuzzy import fuzz
from fuzzywuzzy import process as fuzzy_process

pattern = "Ivermectina é eficaz contra a covid-19"
candidates = ['Própria fabricante diz que ivermectina não tem eficácia contra a covid-19','Análise de estudos sobre ivermectina indica eficácia potencial contra Covid-19','Deputado engana ao dizer que ivermectina é eficaz contra covid-19']



for candidate, score in fuzzy_process.extract(pattern.lower(), list(map(lambda x: x.lower(), candidates)), scorer=fuzz.partial_ratio, limit=1):
    print(candidate, score)