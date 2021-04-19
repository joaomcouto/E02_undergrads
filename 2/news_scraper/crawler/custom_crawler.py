from crawler.base_crawler import BaseCrawler
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class CustomCrawler(BaseCrawler):
    """
    Standart crawler that takes steps to extract data from patterns
    """

    def __init__(self, interface=False):
        """
        Initialize drive and parameters for execution
        """
        # Parameters for execution
        self.try_rate = 15
        wait_rate = 8
        # Choosing browser based on iterface parameter
        if interface:
            super(CustomCrawler, self).__init__("firefox")
        else:
            super(CustomCrawler, self).__init__()
        # Initialize wait object
        self.wait = WebDriverWait(self.driver, wait_rate)

    def get_news(self, url_news, elements, wait_page=None):
        """
        Execute scraper for a news page from a specfic series of steps
        """
        # Load news page
        self.driver.get(url_news)
        # If page has JS
        if wait_page:
            element, selector = wait_page
            self.wait.until(
                EC.presence_of_element_located(
                    (element, selector)
                )
            )
        # Loop over every element that will be scraped
        data = {}
        for key, proccess in elements.items():
            # aux is a transition variable and in the last loop
            # it will store the result:
            aux = None
            try_cnt = 1
            while(try_cnt < self.try_rate):
                try:
                    for step in proccess:
                        type, element, selector = step
                        if type == 'get_text':
                            aux = aux.text
                        elif type == 'verify_existence':
                            if self.driver.findElements(element, selector).isEmpty():
                                break
                        elif type == 'single_element':
                            aux = self.driver.find_element(element, selector)
                        elif type == 'multi_elements':
                            aux = self.driver.find_elements(element, selector)
                        elif type == 'function':
                            pass
                        data.update({key: aux})
                    break
                except:
                    try_cnt += 1
        print(data)

    def close_connection(self):
        self.driver.close()
