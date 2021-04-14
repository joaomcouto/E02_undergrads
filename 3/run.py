# import newspaper

# cnn_paper = newspaper.build('https://g1.globo.com/')

# for article in cnn_paper.articles:
#     print(article.url)

import sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options

PATH = "/home/joaomcouto/chromedriver"
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

driver = webdriver.Chrome(PATH,options=chrome_options)


driver.get("https://g1.globo.com/bemestar/coronavirus/index/feed/pagina-1147.ghtml")
#driver.maximize_window()
#driver.implicitly_wait(10)

delay = 10 # seconds
try:
    myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, "feed-placeholder")))
    print ("Feed encontrado, fazendo varredura...")
except TimeoutException:
    print ("Feed não localizado! Indicativo de varredura completa ou erro de conexão..\n")
    print ("Coletamos",len(URLs), "URLs")
    sys.exit(0)

feedElement = driver.find_element_by_id("feed-placeholder")

materias = feedElement.find_elements_by_xpath('//div[@data-type="materia"]')

URLs = []
for materia in materias:
    URLs.append(materia.find_element_by_tag_name('a').get_attribute('href'))


    #link = materia.find_element_by_xpath('//a')
    #print(link.get_attribute('href'))

#self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#time.sleep(4)

print(URLs)

driver.close()