from crawler.custom.lupa_scraper import LupaScraper
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


def historic_scraper(source, save_rate):
    """
    Controller responsible for executing data collector on historic URLs.
    """
    # Get urls
    urls = select_urls(source)['urls']
    # Initialize variables
    time_success = []
    time_failure = []
    scraped_data = {}
    scraped_htmls = {}
    errors = {}
    current_month = 0
    # Initialize scraper instance
    if source == 'lupa':
        scraper = LupaScraper()
    else:
        scraper = Outline()
    # Execute
    initial_time = time.time()
    for idx, url in enumerate(urls):
        partial_time = time.time()
        try:
            # Execute scraper
            year, month, data, html = scraper.execute(url)
            time_success.append(int(round(abs(partial_time - time.time()), 0)))
            # Every 'save_rate' executions or if the month changes, it saves the collected data
            if idx % save_rate == 0 or current_month != month:
                current_month = month
                # Insert collected data into database
                insert(
                    type='checking',
                    source=source,
                    collected_data=scraped_data,
                    year=year,
                    month=month,
                    url_htmls=scraped_htmls
                    )
                insert(type='error', source=source, collected_data=errors)
                # Clears the dictionaries for new scraped data
                scraped_data = {}
                scraped_htmls = {}
                errors = {}
            scraped_data.update(data)
            scraped_htmls.update({url: html})
        except Exception as e:
            # If a exception is raised during the research, the Exception
            # is saved with the url as keY.
            errors.update({url: str(e)})
            time_failure.append(int(round(abs(partial_time - time.time()), 0)))
    scraper.close_connection()
    full_time = int(round(abs(initial_time - time.time()), 0))
    print(len(urls), " url's scraped in ", full_time, "seconds")
    print("Success mean time: ", statistics.mean(time_success))
    print("Failure mean time: ", statistics.mean(time_failure))
    print('Done')
