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
        if interface:
            super(G1Crawler, self).__init__("firefox")
        else:
            super(G1Crawler, self).__init__()

        self.feedLocator = (By.ID, "feed-placeholder")
        self.materiaLocator = (By.XPATH, '//div[@data-type ="materia"]')
        self.UrlLocator = (By.TAG_NAME , 'a')

        self.delay = 30
        self.retry = 5

        #self.

        # Set wait limit time for elements search
        #self.wait = WebDriverWait(self.driver, self.wait_rate)

    def g1_crawl_pages(self,startPage, endPage, feedUrl):
        URLs = []
        page = startPage
        while (page <= endPage):
            start = time.time()
            self.driver.get(feedUrl + "index/feed/pagina-" + str(page) + ".ghtml")
            try:
                feedElement = WebDriverWait(self.driver, self.delay).until(EC.presence_of_element_located(self.feedLocator))
                print ("Feed encontrado, varrendo pagina", page, "...")
            except TimeoutException:
                if (self.retry == 0):
                    print ("Feed não localizado! Indicativo de varredura completa até a última página do feed ou erro de conexão..\n")
                    break
                else:
                    self.retry = self.retry -1
                    print ("Feed não localizado, tentando novamente") 
                    continue
            materias = feedElement.find_elements(*self.materiaLocator)
            URLCountOnPage = 0
            for materia in materias:
                URLs.append(materia.find_element(*self.UrlLocator).get_attribute('href'))
                URLCountOnPage +=1 
            print("\t", URLCountOnPage, "URLs encontradas em" , round(time.time() - start ,2) ,"segundos" )
            page = page + 1
            self.retry = 3

        fileNameG1 = "G1_" + feedUrl.split('.com/')[1].replace('/' , '_') + str(startPage) + '_a_' + str(page) + ".txt"
        f=open(fileNameG1,'w')
        for u in URLs:
            f.write(u +'\n')
        f.close()
        print (" !!!! Coletamos",len(URLs), "URLs", "em", page-startPage, "paginas")
        self.driver.close()
        sys.exit(0)

    def g1_crawl_all(self,feedUrl):
        self.g1_crawl_pages(1,10000,feedUrl)

#g1 = G1Crawler(0)
#g1.g1_crawl_all("https://g1.globo.com/bemestar/coronavirus/")
#g1.g1_crawl_pages(1150,1153,"https://g1.globo.com/economia/dolar/" )
#g1.g1_crawl_pages(1150,1153,"https://g1.globo.com/bemestar/coronavirus/" )


class UolCrawler(BaseCrawler): #Problema: como escolher o numero de cliques? como saber o que acontece quando nao tem mais pra ver?
    def __init__(self, interface):
        if interface:
            super(UolCrawler, self).__init__("firefox")
        else:
            super(UolCrawler, self).__init__()

        self.feedLocator = (By.CLASS_NAME , 'results-index')
        self.verMaisLocator = (By.XPATH, "//*[contains(text(), 'ver mais')]")
        self.materiaLocator = (By.CLASS_NAME, 'thumbnails-wrapper')
        self.urlLocator = (By.TAG_NAME , 'a')
    
    def uol_crawl_feed(self, feedUrl, clickAmount):
        delay = 10 # seconds
        URLs = []
        self.driver.get(feedUrl)
        #feedElement = self.driver.find_element_by_class_name("results-index")
        feedElement = self.driver.find_element(*self.feedLocator)

        clickAmountDebug = 0
        if(clickAmountDebug == 1):
            repeatRange = 5
        else:
            repeatRange = 2
        for i in range (1, repeatRange):
            for page in range(1,clickAmount):
                start = time.time()
                try:
                    verMaisElement = WebDriverWait(feedElement, delay).until(EC.presence_of_element_located(self.verMaisLocator))
                    print ("Ver Mais encontrado! Clicando pela" , page)
                except TimeoutException:
                    print ("Ver mais não encontrado\n")
                    #printURLs(URLs)
                    print (" !!!! Coletamos",len(URLs), "URLs")
                    driver.close()
                    sys.exit(0)      

                self.driver.execute_script("arguments[0].click();", verMaisElement)

            #materias = feedElement.find_elements_by_class_name('thumbnails-wrapper')
            materias = feedElement.find_elements(*self.materiaLocator)
            URLCountOnPage = 0
            for materia in materias:
                #URLs.append(materia.find_element_by_tag_name('a').get_attribute('href'))
                URLs.append(materia.find_element(*self.urlLocator).get_attribute('href'))
                URLCountOnPage +=1 
            print("\t", URLCountOnPage, "URLs encontradas") # em" , round(time.time() - start ,2) ,"segundos" )



        f=open('Uolteste.txt','w')
        for u in URLs:
            f.write(u +'\n')
        f.close()
        self.driver.close()

#uol = UolCrawler(0)
#uol.uol_crawl_feed("https://noticias.uol.com.br/coronavirus/" , 300)

class BbcCrawler(BaseCrawler):
    def __init__(self, interface):
        if interface:
            super(BbcCrawler, self).__init__("firefox")
        else:
            super(BbcCrawler, self).__init__()

        self.feedLocator = (By.ID, "lx-stream")
        self.materiaLocator = (By.XPATH , '//header[@class ="lx-stream-post__header gs-o-media gs-u-mb-alt"]')
        self.urlLocator = (By.TAG_NAME, 'a')

    def bbc_crawl_pages(self, startPage, endPage, feedUrl):
        delay = 10 # seconds
        URLs = []
        for page in range(startPage,endPage+1):
            start = time.time()
            self.driver.get(feedUrl + "/page/" + str(page))
            #self.driver.get("https://www.bbc.com/portuguese/topics/c340q430z4vt/page/" + str(page))
            try:
                feedElement = WebDriverWait(self.driver, delay).until(EC.presence_of_element_located(self.feedLocator))
                print ("Feed encontrado, varrendo pagina", page, "...")
            except TimeoutException:
                print ("Feed não localizado! Indicativo de varredura completa ou erro de conexão..\n")
                printURLs(URLs)
                print (" !!!! Coletamos",len(URLs), "URLs")
                self.driver.close()
                sys.exit(0)
            time.sleep(2)
            
            #feedElement = self.driver.find_element_by_id("lx-stream")
    

            #materiasHeaders = feedElement.find_elements_by_xpath('//header[@class ="lx-stream-post__header gs-o-media gs-u-mb-alt"]')
            materiasHeaders = feedElement.find_elements(*self.materiaLocator)



            URLCountOnPage = 0
            for materia in materiasHeaders:
                #URLs.append(materia.find_element_by_tag_name('a').get_attribute('href'))
                URLs.append(materia.find_element(*self.urlLocator).get_attribute('href'))
                URLCountOnPage +=1 
            print("\t", URLCountOnPage, "URLs encontradas em" , round(time.time() - start ,2) ,"segundos" )

            f=open('BCC_1_a_100.txt','w')
            for u in URLs:
                f.write(u +'\n')
            f.close()

        printURLs(URLs)
        print (" !!!! Coletamos",len(URLs), "URLs")
        self.driver.close()
        sys.exit(0)

bbc = BbcCrawler(0)
bbc.bbc_crawl_pages(98,100,"https://www.bbc.com/portuguese/topics/c340q430z4vt")


