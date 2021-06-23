import sys
from COLETORES.COLETORES.ADVENTISTAS.ADVENTISTAS_scrapper.py import ADVENTISTASScrapper


def main(argv):
    """
    Select parameters, instanciate source
    than triggers data scraper
    """
    source = argv[0]
    url = argv[1]

    if source == 'adventistas':
        t = ADVENTISTASScrapper(0)

    data = t.scrap_article(url)
    t.append_article_to_txt(data)
    t.driver.quit()


if __name__ == "__main__":
    main(sys.argv[1:])
