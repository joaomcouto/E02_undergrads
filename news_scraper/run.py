from crawler.outline import Outline
import env
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
    interface = False

    if "-init" in argv:
        initialize()

    # Verify interface use:
    if '-I' in argv:
        interface = True

    url_news = argv[-1]
    outline = Outline(interface)
    data = outline.getNews(url_news)
    file_path = os.environ.get('COLLECTED_DIR') + json.loads(data)['title'] + ".json"
    with open(file_path, 'w', encoding='utf8') as json_file:
        json.dump(data, json_file, ensure_ascii=False)


if __name__ == "__main__":
    run(sys.argv[1:])
