import sys
from COLETORES.COLETORES.ADVENTISTAS.ADVENTISTAS_scrapper.py import ADVENTISTASScrapper


def main(argv):
    """
    Select parameters, instanciate source
    than triggers data scraper
    """
    process_type = argv[0]

    if process_type == '-url':
        pass
    elif process_type == '-coletor':
        source = argv[1]
        url = argv[2]
        if source == 'adventistas':
            t = ADVENTISTASScrapper(0)

        data = t.scrap_article(url)
        t.append_article_to_txt(data)
        t.driver.quit()


if __name__ == "__main__":
    main(sys.argv[1:])
