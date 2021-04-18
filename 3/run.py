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
                    print ("Feed não localizado, tentando novamente mais", self.retry +1, "vezes") 
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

        self.delay = 90
    
    def uol_crawl_feed(self, feedUrl, clickAmount):
        self.driver.get(feedUrl)
        feedElement = self.driver.find_element(*self.feedLocator)

        clickAmountDebug = 1
        if(clickAmountDebug == 1):
            repeatRange = 5
        else:
            repeatRange = 2

        for i in range (1, repeatRange+1):
            start = time.time()
            URLs = []
            for click in range(1,clickAmount+1):
                try:
                    verMaisElement = WebDriverWait(feedElement, self.delay).until(EC.presence_of_element_located(self.verMaisLocator))
                    print ("Ver Mais encontrado! Clicando #" , click + ( (i -1) * (clickAmount+1) ))
                except TimeoutException:
                    print ("Ver mais não encontrado . iniciando varredura das materias carregadas\n")
                    break
                self.driver.execute_script("arguments[0].click();", verMaisElement)
            print ("Cliques efetuados em", time.time() - start , "segundos")
            
            start = time.time()
            materias = feedElement.find_elements(*self.materiaLocator)
            for materia in materias:
                URLs.append(materia.find_element(*self.urlLocator).get_attribute('href'))
            print ("Crawl de materias feito em " , time.time() - start)
            print (" !!!! Coletamos",len(URLs), "URLs com" ,click * i, "cliques")

        #fileNameG1 = "G1_" + feedUrl.split('.com/')[1].replace('/' , '_') + str(startPage) + '_a_' + str(page) + ".txt"
        uolFileName = "UOL_" + feedUrl.split('.br/')[1].replace('/' , '_') + str(clickAmount*repeatRange) + "_loads" + ".txt"
        f=open(uolFileName,'w')
        for u in URLs:
            f.write(u +'\n')
        f.close()
        self.driver.close()
        sys.exit(0) 

#uol = UolCrawler(0)
#uol.uol_crawl_feed("https://noticias.uol.com.br/coronavirus/" , 2)

class BbcCrawler(BaseCrawler):
    def __init__(self, interface):
        if interface:
            super(BbcCrawler, self).__init__("firefox")
        else:
            super(BbcCrawler, self).__init__()

        self.feedLocator = (By.ID, "lx-stream")
        self.materiaLocator = (By.XPATH , '//header[@class ="lx-stream-post__header gs-o-media gs-u-mb-alt"]')
        self.urlLocator = (By.TAG_NAME, 'a')


        self.delay = 90
        self.retry = 5

    def bbc_crawl_pages(self, startPage, endPage, feedUrl):
        URLs = []
        page = startPage
        while (page <= endPage):
            start = time.time()
            self.driver.get(feedUrl + "/page/" + str(page))
            try:
                feedElement = WebDriverWait(self.driver, self.delay).until(EC.presence_of_element_located(self.feedLocator))
                print ("Feed encontrado, varrendo pagina", page, "...")
            except TimeoutException:
                if (self.retry == 0):
                    print ("Feed não localizado! Indicativo de varredura completa ou erro de conexão..\n")
                    break
                else:
                    self.retry = self.retry  -1
                    print ("Feed não localizado, tentando novamente mais", self.retry +1, "vezes") 
                    continue
                
            time.sleep(1)
            
            materiasHeaders = feedElement.find_elements(*self.materiaLocator)

            URLCountOnPage = 0
            for materia in materiasHeaders:
                URLs.append(materia.find_element(*self.urlLocator).get_attribute('href'))
                URLCountOnPage +=1 
            print("\t", URLCountOnPage, "URLs encontradas em" , round(time.time() - start ,2) ,"segundos" )
            page = page + 1
            self.retry = 3

        print (" !!!! Coletamos",len(URLs), "URLs")
        bbcFileName = "BCC_" + feedUrl.split('portuguese/')[1].replace('/' , '_') + "_" + str(startPage) + '_a_' + str(page-1) + ".txt"
        f=open(bbcFileName,'w')
        for u in URLs:
            f.write(u +'\n')
        f.close()
        
        self.driver.close()
        sys.exit(0)


bbc = BbcCrawler(0)
bbc.bbc_crawl_pages(99,104,"https://www.bbc.com/portuguese/topics/c340q430z4vt")


