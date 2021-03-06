import os
import env
import sys
import time

from news_crawler.base_crawler import BaseCrawler

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import StaleElementReferenceException

from selenium.webdriver.chrome.options import Options


def printURLs(lista):
    for URL in lista:
        print(URL, "\n")

def fetch_latest_5(fileName):
    with open(fileName) as myfile:
        head = [next(myfile).strip("\n") for x in range(5)]
    return head

def line_prepender(filename, line):
    with open(filename, 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        f.write(line.rstrip('\r\n') + '\n' + content)

def file_to_urls(fileName):
    URLs = []
    f=open(fileName,'r')
    for line in f:
        URLs.append(line.strip("\n"))
    f.close()
    return URLs

def remove_list_duplicates(inputList):
    seen = set()
    seen_add = seen.add
    return [x for x in inputList if not (x in seen or seen_add(x))]


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


    def update(self, feedUrl,fileName):
        latest = fetch_latest_5(fileName)
        latestFromFeed = file_to_urls(self.g1_crawl_pages(1,60,feedUrl))
        toAdd = []
        for i,materia in enumerate(latestFromFeed):
            if materia in latest[1:]:
                if (latestFromFeed[i+1] in latest[1:]):
                    if (latestFromFeed[i+2] in latest[1:]):
                        break
            else:
                toAdd.append(materia)
            
        for materia in reversed(toAdd):
            line_prepender(fileName, materia)

    def g1_crawl_pages(self,startPage, endPage, feedUrl):
        URLs = []
        page = startPage
        while (page <= endPage):
            if(page > 2000): #Necessario pois ap??s 2000 p??ginas o G1 carrega sempre o feed da pagina 2000, entao a excess??o de parada n??o acontece
                print ('Ultima pagina poss??vel alcan??ada')
                break
            start = time.time()
            pageURLs = self.g1_crawl_single_page(feedUrl,page)
            if (pageURLs == -1):
                print ("Feed n??o localizado! Indicativo de varredura completa at?? a ??ltima p??gina DISPONIVEL do feed ou erro de conex??o..\n")
                break
            if (pageURLs == 0):
                self.retry = self.retry -1
                print ("Feed n??o localizado, tentando novamente mais", self.retry +1, "vezes") 
                continue
            print("\t", len(pageURLs), "URLs encontradas em" , round(time.time() - start ,2) ,"segundos" )
            URLs.extend(pageURLs)
            page = page + 1
            self.retry = 3

        print (" !!!! Coletamos",len(URLs), "URLs", "em", page-startPage, "paginas")
        URLs = remove_list_duplicates(URLs)

        fileName = self.g1_urls_to_file(URLs,feedUrl,startPage,page)
        return fileName
        #self.driver.close()
        #sys.exit(0)

    def g1_crawl_all(self,feedUrl):
        feedUrlsFile = self.g1_crawl_pages(1,2000,feedUrl)
        newName = "G1_" + feedUrl.split('.com/')[1].replace('/' , '_') + "all"
        os.rename(feedUrlsFile,newName)


    def g1_urls_to_file(self,URLs, feedUrl, startPage,page):
        fileNameG1 = "G1_" + feedUrl.split('.com/')[1].replace('/' , '_') + str(startPage) + '_a_' + str(page) + ".txt"
        f=open(fileNameG1,'w')
        for u in URLs:
            f.write(u +'\n')
        f.close()
        return fileNameG1

    
    def g1_crawl_single_page(self,feedUrl, page):
        pageURLs = []
        self.driver.get(feedUrl + "index/feed/pagina-" + str(page) + ".ghtml")
        try:
            feedElement = WebDriverWait(self.driver, self.delay).until(EC.presence_of_element_located(self.feedLocator))
            print ("Feed encontrado, varrendo pagina", page, "...")
        except TimeoutException:
            if (self.retry == 0):
                return -1
            else:
                return 0
        materias = feedElement.find_elements(*self.materiaLocator)
        for materia in materias:
            pageURLs.append(materia.find_element(*self.UrlLocator).get_attribute('href'))        
        return pageURLs
        
#g1 = G1Crawler(0)
#g1.g1_crawl_all("https://g1.globo.com/fato-ou-fake/")
#"https://g1.globo.com/fato-ou-fake/"
#g1.g1_crawl_pages(1150,1153,"https://g1.globo.com/economia/dolar/" )
#g1.g1_crawl_pages(1,10,"https://g1.globo.com/bemestar/coronavirus/" )
#g1.update("https://g1.globo.com/bemestar/coronavirus/", "G1/URL/G1_bemestar_coronavirus_historica_may_24.txt")
#g1.file_to_urls("G1_bemestar_coronavirus_1_a_11.txt")
#g1.driver.close()


class UolCrawler(BaseCrawler): #Problema: como escolher o numero de cliques? como saber o que acontece quando nao tem mais pra ver?
    def __init__(self, interface):
        if interface:
            super(UolCrawler, self).__init__("firefox")
        else:
            super(UolCrawler, self).__init__()

        #self.feedLocator = (By.CLASS_NAME , 'results-index')
        self.feedLocator = (By.CLASS_NAME , 'results-items')
        self.verMaisLocator = (By.XPATH, "//*[contains(text(), 'ver mais')]")
        self.materiaLocator = (By.CLASS_NAME, 'thumbnails-wrapper')
        #self.materiaLocator = (By.CLASS_NAME, 'thumbnails-item.align-horizontal.list.col-xs-8.col-sm-12.small.col-sm-24.small')
        self.urlLocator = (By.TAG_NAME , 'a')

        self.delay = 90
    
    def uol_crawl_feed(self, feedUrl, clickAmount):
        self.driver.get(feedUrl)
        feedElement = self.driver.find_element(*self.feedLocator)

        clickAmountDebug = 0
        if(clickAmountDebug == 1):
            repeatRange = 5
        else:
            repeatRange = 2
        for i in range (1, repeatRange):
            start = time.time()
            URLs = []
            for click in range(1,clickAmount+1):
                latestClick = time.time()
                clickRet = self.uol_ver_mais(feedElement)
                if (clickRet == 0):
                    print ("Ver mais n??o encontrado . Iniciando varredura das materias carregadas\n")
                    break
                else:
                    print ("Ver Mais encontrado! Clicando #" , click + ( (i -1) * (clickAmount) ),"tempo corrente:",time.time() - start, "tempo unitario:", time.time()-latestClick)
            print ("Cliques efetuados em", time.time() - start , "segundos")
            
            start = time.time()
            try:
                materias = feedElement.find_elements(*self.materiaLocator)
            except StaleElementReferenceException:
                materias = feedElement.find_elements(*self.materiaLocator)

            count = 0 
            totalMaterias = len(materias)
            print (" !! Achamos",totalMaterias, "elementos de materia com" ,click * i, "cliques")
            for materia in materias:
                latest = time.time()
                URLs.append(materia.find_element(*self.urlLocator).get_attribute('href'))
                count += 1
                print("Crawl materia #" ,count, "/",totalMaterias, " tempo corrente:", time.time() - start , "tempo unitario:", time.time() - latest)
            print ("Crawl de materias feito em " , time.time() - start)
            print (" !!!! Coletamos",len(URLs), "URLs com" ,click * i, "cliques")
        
        URLs = remove_list_duplicates(URLs)
        self.uol_urls_to_file(clickAmount, repeatRange, feedUrl, URLs)

        self.driver.close()
        sys.exit(0) 

    def uol_urls_to_file(self,clickAmount, repeatRange, feedUrl, URLs):
        uolFileName = "UOL_" + feedUrl.split('.br/')[1].replace('/' , '_') + str(clickAmount*(repeatRange-1)) + "_loads" + ".txt"
        f=open(uolFileName,'w')
        for u in URLs:
            f.write(u +'\n')
        f.close()

    def uol_ver_mais(self,feedElement):
        try:
            verMaisElement = WebDriverWait(feedElement, self.delay).until(EC.presence_of_element_located(self.verMaisLocator))
        except TimeoutException:
            return 0
        except StaleElementReferenceException:
            return 0
        self.driver.execute_script("arguments[0].click();", verMaisElement)
        return 1

uol = UolCrawler(0)
uol.uol_crawl_feed("https://noticias.uol.com.br/coronavirus/" , 441)
uol.driver.quit()

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
            pageUrls = self.bbc_crawl_single_page(page, feedUrl)
            if pageUrls == -1:
                print ("Feed n??o localizado! Indicativo de varredura completa ou erro de conex??o..\n")
                break
            if pageUrls == 0:
                self.retry = self.retry  -1
                print ("Feed n??o localizado, tentando novamente mais", self.retry +1, "vezes") 
                continue
            URLs.extend(pageUrls)
            page = page + 1
            self.retry = 3
        print (" !!!! Coletamos",len(URLs), "URLs")
        URLs = remove_list_duplicates(URLs)
        self.bbc_urls_to_file(startPage,page, URLs, feedUrl)
        self.driver.close()
        sys.exit(0)
    
    def bbc_urls_to_file(self,startPage, endPage, URLs,feedUrl):
        bbcFileName = "BCC_" + feedUrl.split('portuguese/')[1].replace('/' , '_') + "_" + str(startPage) + '_a_' + str(endPage-1) + ".txt"
        f=open(bbcFileName,'w')
        for u in URLs:
            f.write(u +'\n')
        f.close()

    def bbc_crawl_single_page(self, page, feedUrl):
        pageUrls = []
        start = time.time()
        self.driver.get(feedUrl + "/page/" + str(page))
        try:
            feedElement = WebDriverWait(self.driver, self.delay).until(EC.presence_of_element_located(self.feedLocator))
            print ("Feed encontrado, varrendo pagina", page, "...")
        except TimeoutException:
            if (self.retry == 0):
                return -1
            else:
                return 0
        time.sleep(1)
        materiasHeaders = feedElement.find_elements(*self.materiaLocator)
        URLCountOnPage = 0
        for materia in materiasHeaders:
            pageUrls.append(materia.find_element(*self.urlLocator).get_attribute('href'))
            URLCountOnPage +=1 
        print("\t", URLCountOnPage, "URLs encontradas em" , round(time.time() - start ,2) ,"segundos" )
        return pageUrls


        
        
#bbc = BbcCrawler(0)
#x`a = bbc.bbc_crawl_pages(99,104,"https://www.bbc.com/portuguese/topics/c340q430z4vt")
#MANO ESSE TEMPO TODO TU FEZ O LINK ERRADO O DO CORONA EH ESSE AQUI:
#https://www.bbc.com/portuguese/topics/clmq8rgyyvjt


