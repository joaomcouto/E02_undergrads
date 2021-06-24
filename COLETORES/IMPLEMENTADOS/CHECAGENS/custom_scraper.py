from abc import ABC, abstractmethod
from selenium.webdriver.support.ui import WebDriverWait
import hashlib
import os
import json

from COLETORES.IMPLEMENTADOS.CHECAGENS.base_crawler import BaseCrawler


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
        self.try_rate = 3
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

    def insert(self, type, collected_data, html=None, year=0, month=0):
        """
        Receives errors or checking news in json format
        and inserts it on text-json database file.
        """
        source = self.source
        source_folder = os.environ.get('CHECAGENS') + source + '/'
        if type == 'checking':
            html_folder = source_folder + 'HTML/'
            if month < 10:
                month = '0' + str(month)
            file_path = source_folder + f'COLETA/{source}_{year}_{month}.txt'
        elif type == 'error':
            file_path = source_folder + 'LOG/not_collected.json'
        else:
            raise 'DataBase error(Invalid type on json database file)'
        try:
            # SAVING HTMLs
            if type == 'checking':
                hash_value = collected_data['raw_file_name']
                with open(f'{html_folder}{hash_value}.html', "w") as file:
                    file.write(html)
            # SAVING COLLECTED DATA
            with open(file_path, mode='a', encoding='utf-8') as f:
                f.write(json.dumps(collected_data, ensure_ascii=False) + '\n')
        except Exception as e:
            print(e)
            print("Problem while saving data")
            raise e
