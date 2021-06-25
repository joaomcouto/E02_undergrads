import json
import pprint


def lendo_dataset(localizacao_arquivo):
    # Leitura de dados:
    dados = []
    with open(localizacao_arquivo, mode='r') as f:
        for line in f:
            dados.append(json.loads(line.strip()))

    # Imprimindo primeiro 3 coletas de cada
    for i in range(3):
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(dados[i])
        print('\n')


# Lendo TrueNews
print('\n---------------TRUE NEWS:\n')
lendo_dataset('../data/DATASET_MPMG-TrueNews_selected.txt')

print('\n\n\n---------------FAKE NEWS:\n')
# Lendo FakeNews
lendo_dataset('../data/DATASET_MPMG-FakeNews_matched.txt')
