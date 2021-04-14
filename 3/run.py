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

def printURLs(lista):
    for URL in lista:
        print(URL, "\n")

def crawler_g1_pages(startPage, endPage):
    delay = 10 # seconds
    URLs = []
    for page in range(startPage,endPage):
        start = time.time()
        driver.get("https://g1.globo.com/bemestar/coronavirus/index/feed/pagina-" + str(page) + ".ghtml")
        try:
            myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, "feed-placeholder")))
            print ("Feed encontrado, varrendo pagina", page, "...")
        except TimeoutException:
            print ("Feed não localizado! Indicativo de varredura completa ou erro de conexão..\n")
            printURLs(URLs)
            print (" !!!! Coletamos",len(URLs), "URLs")
            driver.close()
            sys.exit(0)

        
        feedElement = driver.find_element_by_id("feed-placeholder")

        materias = feedElement.find_elements_by_xpath('//div[@data-type ="materia"]')

        URLCount = 0
        for materia in materias:
            URLs.append(materia.find_element_by_tag_name('a').get_attribute('href'))
            URLCount +=1 
        print("\t", URLCount, "URLs encontradas em" , round(time.time() - start ,2) ,"segundos" )

        f=open('G1_1140_a_1150.txt','w')
        for u in URLs:
            f.write(u +'\n')
        f.close()

#crawler_g1_pages(1140,1150)

def crawler_uol():
    delay = 10 # seconds
    URLs = []
    driver.get("https://noticias.uol.com.br/coronavirus/")
    feedElement = driver.find_element_by_class_name("results-index")
    for i in range (1, 5):
        for page in range(1,50):
            start = time.time()
            try:
                myElem = WebDriverWait(feedElement, delay).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'ver mais')]")))
                print ("Ver Mais encontrado! Clicando pela" , page)
            except TimeoutException:
                print ("Ver mais não encontrado\n")
                printURLs(URLs)
                print (" !!!! Coletamos",len(URLs), "URLs")
                driver.close()
                sys.exit(0)      

            verMaisElement = feedElement.find_element_by_xpath("//button[contains(text(), 'ver mais')]")
            driver.execute_script("arguments[0].click();", verMaisElement)

        materias = feedElement.find_elements_by_xpath('//div[@class ="thumbnails-wrapper"]')
        URLCount = 0
        for materia in materias:
            URLs.append(materia.find_element_by_tag_name('a').get_attribute('href'))
            URLCount +=1 
        print("\t", URLCount, "URLs encontradas") # em" , round(time.time() - start ,2) ,"segundos" )

        # f=open('G1_1140_a_1150.txt','w')
        # for u in URLs:
        #     f.write(u +'\n')
        # f.close()
    driver.close()

crawler_uol()


