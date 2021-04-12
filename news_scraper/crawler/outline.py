from crawler.base_crawler import BaseCrawler
import json
from newspaper import Article
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time


class Outline(BaseCrawler):
    """
    Initialize a webdriver from Base crawler.
    Receives a news url, using selenium passes this news to outline.
    Scrapes the outline new html and passes to newspaper3k who separate
    the news data.
    """

    def __init__(self, interface):
        """
        Create chosen base crawler driver and
        set the parameters for scraping.
        """
        # Choosing browser based on iterface parameter
        if interface:
            super(Outline, self).__init__("firefox")
        else:
            super(Outline, self).__init__()

        # Parameters:
        self.wait_rate = 180
        self.outline_url = "https://outline.com/"

        # Set wait limit time for elements search
        self.wait = WebDriverWait(self.driver, self.wait_rate)

    def getNews(self, url_news):
        """
        Receives a news url and return a json data.
        """
        html, outline_url, date = self.__get_html_with_selenium(url_news)
        article = self.__get_article_with_newspaper3k(url_news, html)
        results = self.__format_result(
            url_news,
            outline_url,
            date,
            article)
        self.driver.close()
        return results

    def __get_html_with_selenium(self, url_news):
        """
        Passes the url to outline, scrapes and return
        the html, the outline url and date of the news.
        """
        # Access outline website
        self.driver.get(self.outline_url)
        time.sleep(3)
        # Select url box
        url_box_input = self.driver.find_element_by_id("source")
        time.sleep(1)
        # Fill the url box:
        url_box_input.send_keys(url_news)
        time.sleep(2)
        # Click on create outline:
        self.driver.find_element_by_class_name("clean").click()
        # Wait javascript to load:
        self.wait.until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, "article-wrapper"))
            )
        time.sleep(2)
        # Get the data:
        html = self.driver.page_source
        outline_url = self.driver.current_url
        date_element = self.driver.find_element_by_class_name("date")
        date = date_element.get_attribute("innerHTML")
        return html, outline_url, date

    def __get_article_with_newspaper3k(self, url_news, html):
        """
        Create a Article object using html retrieved by selenium.
        """
        article = Article(url_news, language='pt')
        # set html manually:
        article.html = html
        # Change the status so don't have to download the article from a url:
        article.download_state = 2
        article.parse()
        return article

    def __format_result(self, url_news, outline_url, date, article):
        """
        Returns a json with all scraped data from news.
        """
        article.nlp()
        results = {
            'font': url_news,
            'outline-url': outline_url,
            'title': article.title,
            'date': date,
            'img': list(article.images),
            'key-words': article.keywords,
            'summary': article.summary,
            'text': article.text
        }
        print(results)
        return json.dumps(results)
