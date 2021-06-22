from controller.scrapers import scrape
import sys


def run(argv):
    source = argv[-1][1:]
    possible_sources = [
        'aos_fatos',
        'boatos',
        'fato-ou=fake',
        'lupa'
    ]
    if source in possible_sources:
        scrape(source)
    else:
        print("Por favor especifique um coletor válido")


if __name__ == "__main__":
    run(sys.argv[1:])
