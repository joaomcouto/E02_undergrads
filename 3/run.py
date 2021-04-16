# import newspaper

# cnn_paper = newspaper.build('https://g1.globo.com/')

# for article in cnn_paper.articles:
#     print(article.url)

import os
import env


from news_crawler.base_crawler import BaseCrawler

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


def printURLs(lista):
    for URL in lista:
        print(URL, "\n")


class G1Crawler(BaseCrawler):
    def __init__(self, interface):
        """
        Create chosen base crawler driver 
        """
        # Choosing browser based on iterface parameter
        if interface:
            super(G1Crawler, self).__init__("firefox")
        else:
            super(G1Crawler, self).__init__()

        # Parameters:
        #self.wait_rate = 180
        #self.outline_url = "https://outline.com/"

        # Set wait limit time for elements search
        #self.wait = WebDriverWait(self.driver, self.wait_rate)

    def g1_crawl_pages(self,startPage, endPage, feedUrl):
        delay = 10 # seconds
        URLs = []
        for page in range(startPage,endPage+1):
            start = time.time()
            self.driver.get(feedUrl + "index/feed/pagina-" + str(page) + ".ghtml")
            #self.driver.get("https://g1.globo.com/bemestar/coronavirus/index/feed/pagina-" + str(page) + ".ghtml")
            try:
                myElem = WebDriverWait(self.driver, delay).until(EC.presence_of_element_located((By.ID, "feed-placeholder")))
                print ("Feed encontrado, varrendo pagina", page, "...")
            except TimeoutException:
                print ("Feed não localizado! Indicativo de varredura completa ou erro de conexão..\n")
                #printURLs(URLs)
                print (" !!!! Coletamos",len(URLs), "URLs")
                self.driver.close()
                sys.exit(0)

            
            feedElement = self.driver.find_element_by_id("feed-placeholder")

            materias = feedElement.find_elements_by_xpath('//div[@data-type ="materia"]')

            URLCount = 0
            for materia in materias:
                URLs.append(materia.find_element_by_tag_name('a').get_attribute('href'))
                URLCount +=1 
            print("\t", URLCount, "URLs encontradas em" , round(time.time() - start ,2) ,"segundos" )

            f=open('G1_' + str(startPage) + '_a_' + str(endPage) + ".txt",'w')
            for u in URLs:
                f.write(u +'\n')
            f.close()

    def g1_crawl_all(self,feedUrl):
        self.g1_crawl_pages(1,10000,feedUrl)

g1 = G1Crawler(0)
g1.g1_crawl_all("https://g1.globo.com/bemestar/coronavirus/")


class UolCrawler(BaseCrawler):
    def __init__(self, interface):
        if interface:
            super(UolCrawler, self).__init__("firefox")
        else:
            super(UolCrawler, self).__init__()

    # Parameters:
    #self.wait_rate = 180
    #self.outline_url = "https://outline.com/"

    # Set wait limit time for elements search
    #self.wait = WebDriverWait(self.driver, self.wait_rate)

    def uol_crawl_feed(self):
        delay = 10 # seconds
        URLs = []
        self.driver.get("https://noticias.uol.com.br/coronavirus/")
        feedElement = self.driver.find_element_by_class_name("results-index")
        for i in range (1, 5):
            for page in range(1,5):
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
                self.driver.execute_script("arguments[0].click();", verMaisElement)

            #materias = feedElement.find_elements_by_xpath('//div/div/div/div/div[@class ="thumbnails-wrapper"]')
            materias = feedElement.find_elements_by_class_name('thumbnails-wrapper')
            URLCount = 0
            for materia in materias:
                URLs.append(materia.find_element_by_tag_name('a').get_attribute('href'))
                URLCount +=1 
            print("\t", URLCount, "URLs encontradas") # em" , round(time.time() - start ,2) ,"segundos" )

            # f=open('G1_1140_a_1150.txt','w')
            # for u in URLs:
            #     f.write(u +'\n')
            # f.close()
        self.driver.close()

#uol = UolCrawler(1)
#uol.uol_crawl_feed()

class BbcCrawler(BaseCrawler):
    def __init__(self, interface):
        if interface:
            super(BbcCrawler, self).__init__("firefox")
        else:
            super(BbcCrawler, self).__init__()

    def bbc_crawl_pages(self, startPage, endPage):
        delay = 10 # seconds
        URLs = []
        for page in range(startPage,endPage+1):
            start = time.time()
            self.driver.get(feedUrl + "/page/" + str(page))
            self.driver.get("https://www.bbc.com/portuguese/topics/c340q430z4vt/page/" + str(page))
            try:
                myElem = WebDriverWait(self.driver, delay).until(EC.presence_of_element_located((By.ID, "lx-stream")))
                print ("Feed encontrado, varrendo pagina", page, "...")
            except TimeoutException:
                print ("Feed não localizado! Indicativo de varredura completa ou erro de conexão..\n")
                printURLs(URLs)
                print (" !!!! Coletamos",len(URLs), "URLs")
                self.driver.close()
                sys.exit(0)
            time.sleep(2)
            
            #feedElement = self.driver.find_element_by_id("lx-stream")
            feedElement = myElem

            materiasHeaders = feedElement.find_elements_by_xpath('//header[@class ="lx-stream-post__header gs-o-media gs-u-mb-alt"]')

            URLCount = 0
            for materia in materiasHeaders:
                URLs.append(materia.find_element_by_tag_name('a').get_attribute('href'))
                URLCount +=1 
            print("\t", URLCount, "URLs encontradas em" , round(time.time() - start ,2) ,"segundos" )

            f=open('BCC_1_a_100.txt','w')
            for u in URLs:
                f.write(u +'\n')
            f.close()

        printURLs(URLs)
        print (" !!!! Coletamos",len(URLs), "URLs")
        self.driver.close()
        sys.exit(0)

bbc = BbcCrawler(0)
bbc.bbc_crawl_pages(99,100)


