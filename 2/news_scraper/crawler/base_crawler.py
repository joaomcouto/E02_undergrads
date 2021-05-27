import os  # Allow use of shell commands
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class BaseCrawler:
    """
    Given the choice of which drive will be used,
    it is created and the arguments are configured.
    """

    def __init__(self, browser="chrome_headless"):
        # Browser headless, for automatic execution
        if browser == "chrome_headless":
            driver_dir = os.environ.get('CHROME')
            chrome_options = self.__set_chrome_options()
            self.driver = webdriver.Chrome(options=chrome_options,
                                           executable_path=driver_dir)
        # Browser for visual execution
        elif browser == "firefox":
            driver_dir = os.environ.get('FIREFOX')
            self.driver = webdriver.Firefox(executable_path=driver_dir)

    def __set_chrome_options(self):
        """
        Set arguments for headless chome.
        """
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=1920x1080")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--verbose')
        chrome_options.add_experimental_option("prefs", {
            "download.default_directory": "",
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing_for_trusted_sources_enabled": False,
            "safebrowsing.enabled": False
        })
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-software-rasterizer')

        return chrome_options

    def close_connection(self):
        self.driver.close()
