from crawler.custom_crawler import CustomCrawler
from crawler.outline import Outline
from mapper.json_db_mapper import get_database_json_format
from mapper.url_mapper import get_source_information
from repository.json_db import insert_multiple_news
from repository.json_db import select_urls
import time


def scrape():
    """
    Controller responsible for executing routine of data collector.
    """
    # Get urls
    urls = select_urls()['urls']
    # Initialize dictionaries to store results
    formatted_news = {}
    formatted_checking = {}
    # Initialize scrapers objects
    outline = Outline()
    custom_crawler = CustomCrawler()
    # Execute
    initial_time = time.time()
    for url in urls:
        partial_time = time.time()
        source, information = get_source_information(url)
        # Select type of search by url source
        if information['has_custom_crawler']:
            data = custom_crawler.get_news(
                url_news=url,
                elements=information['elements'],
                wait_page=information['has_js'])
        else:
            data = outline.get_news(url)
        json_formatted = get_database_json_format(source, data)
        if information['type'] == 'fact_checking':
            formatted_checking.update(json_formatted)
        elif information['type'] == 'news':
            formatted_news.update(json_formatted)
        else:
            raise 'Unspecified url type for database insertion of collected data'
        this_time = int(round(abs(partial_time - time.time()), 0))
        print(source, " url scraped in ", this_time, " seconds")

    outline.close_connection()
    custom_crawler.close_connection()
    full_time = int(round(abs(initial_time - time.time()), 0))
    print(len(urls), " url's scraped in ", full_time, "seconds")
    print('Saving data on database...')
    # Insert collected data into database
    insert_multiple_news(type='news', collected_data=formatted_news)
    insert_multiple_news(type='checking', collected_data=formatted_checking)
    print('Done')
