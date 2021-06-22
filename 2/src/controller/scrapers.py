from crawler.custom.aos_fatos_scraper import AosFatosScraper
from crawler.custom.boatos_scraper import BoatosScraper
from crawler.custom.fato_ou_fake_scraper import FatoOuFakeScraper
from crawler.custom.lupa_scraper import LupaScraper
from repository.json_db import insert
from repository.json_db import select_urls


def scrape(source):
    """
    Controller responsible for executing data collector on historic URLs.
    """
    # Get urls
    urls = select_urls(source)['urls']
    # Initialize time lists
    # Initialize scraper instance
    if source == 'lupa':
        scraper = LupaScraper()
    elif source == 'aos_fatos':
        scraper = AosFatosScraper()
    elif source == 'fato-ou-fake':
        scraper = FatoOuFakeScraper()
    elif source == 'boatos':
        scraper = BoatosScraper()

    # Execute
    for url in urls:
        try:
            # Execute scraper
            year, month, data, html = scraper.execute(url)
            # Insert collected data into database
            insert(
                type='checking',
                source=source,
                collected_data=data,
                html=html,
                year=year,
                month=month
                )
        except Exception as e:
            # If a exception is raised during the research, the Exception
            # is saved with the url as keY.
            insert(
                type='error',
                source=source,
                collected_data={url: str(e)}
                )
    scraper.close_connection()
