from crawler.outline import Outline
import nltk
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
    print(data)


if __name__ == "__main__":
    run(sys.argv[1:])
