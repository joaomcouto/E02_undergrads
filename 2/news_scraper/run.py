from crawler.outline import Outline
from controller.scrapers import scrape
from test.aosfatos import aos_fatos_test
import json
import nltk
import os
import sys


def initialize():
    """
    Execute initial commands for enviroment.
    """
    # necessary for nlp in newspaper library:
    nltk.download('punkt')


def run(argv):
    """
    Execute and generate json file.
    """
    # Verify inicialization argument
    if "-init" in argv:
        initialize()

    # Verify interface use for single news scrape:
    if '--interface' in argv or '-I' in argv:
        url_news = argv[-1]
        outline = Outline(interface=True)
        data = outline.getNews(url_news)
        file_path = os.environ.get('COLLECTED_DIR') + json.loads(data)['title'] + ".json"
        with open(file_path, 'w', encoding='utf8') as json_file:
            json.dump(data, json_file, ensure_ascii=False)

    # Verify for routine execution
    if '--routine' in argv or '-r' in argv:
        scrape()


if __name__ == "__main__":
    run(sys.argv[1:])
