from abc import ABC, abstractmethod
from crawler.base_crawler import BaseCrawler
import hashlib
from selenium.webdriver.support.ui import WebDriverWait


class CustomScraper(ABC):
    """
    Abstract class that has a constructor and BaseCrawler as inner class.
    This class implements the rules for custom crawlers.
    """

    def __init__(self, interface=False):
        """
        Initialize drive and parameters for execution.
        """
        # Parameters for execution
        self.try_rate = 15
        wait_rate = 8
        # Instanciate BaseCraler as inner Class so it doesn't violate the
        # pattern of abstract classes.
        if interface:
            # Choosing browser based on iterface parameter
            self.driver = BaseCrawler("firefox").driver
        else:
            self.driver = BaseCrawler().driver
        # Initialize wait object
        self.wait = WebDriverWait(self.driver, wait_rate)

    @abstractmethod
    def get_title(self):
        pass

    @abstractmethod
    def get_subtitle(self):
        pass

    @abstractmethod
    def get_date(self):
        pass

    @abstractmethod
    def get_authors(self):
        pass

    @abstractmethod
    def get_text(self):
        pass

    @abstractmethod
    def get_categories(self):
        pass

    @abstractmethod
    def get_tags(self):
        pass

    @abstractmethod
    def get_veredicts(self):
        pass

    @abstractmethod
    def get_image(self):
        pass

    @abstractmethod
    def get_video(self):
        pass

    @abstractmethod
    def get_html():
        pass

    @abstractmethod
    def execute(self, url):
        pass

    def close_connection(self):
        self.driver.close()

    def get_html_file_value(self, url):
        """
        Receives url and returns unique value.
        This unique value corresponds to the html file.
        """
        return hashlib.sha1(url.encode()).hexdigest()
