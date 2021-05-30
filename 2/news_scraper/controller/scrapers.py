from crawler.custom.lupa_scraper import LupaScraper
from crawler.custom.aos_fatos_scraper import AosFatosScraper
from crawler.custom.fato_ou_fake_scraper import FatoOuFakeScraper
from crawler.outline import Outline
from repository.json_db import insert
from repository.json_db import select_urls
import time
import statistics


def routine_scraper():
    """
    Controller responsible for executing routine of data collector.
    """
    pass


def historic_scraper(source):
    """
    Controller responsible for executing data collector on historic URLs.
    """
    # Get urls
    urls = select_urls(source)['urls']
    # Initialize time lists
    time_success = []
    time_failure = []
    # Initialize scraper instance
    if source == 'lupa':
        scraper = LupaScraper()
    elif source == 'aos_fatos':
        scraper = AosFatosScraper()
    elif source == 'fato-ou-fake':
        scraper = FatoOuFakeScraper()
    else:
        scraper = Outline()
    # Execute
    initial_time = time.time()
    for url in urls:
        partial_time = time.time()
        try:
            # Execute scraper
            year, month, data, html = scraper.execute(url)
            time_success.append(int(round(abs(partial_time - time.time()), 0)))
            # Insert collected data into database
            insert(
                url='url',
                type='checking',
                source=source,
                collected_data=data,
                html=html,
                year=year,
                month=month
                )
            time_success.append(int(round(abs(partial_time - time.time()), 0)))
        except Exception as e:
            # If a exception is raised during the research, the Exception
            # is saved with the url as keY.
            insert(
                url=url,
                type='error',
                source=source,
                collected_data={url: str(e)}
                )
            time_failure.append(int(round(abs(partial_time - time.time()), 0)))
    scraper.close_connection()
    full_time = int(round(abs(initial_time - time.time()), 0))
    print(len(urls), " url's scraped in ", full_time, "seconds")
    print("Success mean time: ", statistics.mean(time_success))
    print("Failure mean time: ", statistics.mean(time_failure))
    print('Done')
