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
from selenium.webdriver.chrome.options import Options

class G1Scrapper(BaseCrawler):
    def __init__(self,interface):
        if interface:
            super(G1Scrapper, self).__init__("firefox")
        else:
            super(G1Scrapper, self).__init__()

        self.text_locator = (By.CLASS_NAME,'content-text__container')
        self.subtitle_locator = (By.CLASS_NAME,'content-head__subtitle')
        self.title_locator =(By.CLASS_NAME,'content-head__title')
        self.image_locator = (By.TAG_NAME,'amp-img')
        self.author_locator =  (By.CLASS_NAME , 'content-publication-data__from')
        self.category_locator =(By.CLASS_NAME,'header-editoria--link.ellip-line')
        self.main_wrapper_locator = (By.CLASS_NAME, 'mc-body.theme')
        self.date_locator = (By.XPATH, '//time[@itemprop = "datePublished"]')
        self.type = "noticia"
        self.fonte = "G1"
        self.video_locator = (By.CLASS_NAME, "content-video__placeholder")



    def access_article(self, articleUrl):
        self.driver.get(articleUrl)

    def get_text(self):
        ret = ""
        trechos = self.currentWrapper.find_elements(*self.text_locator)
        for trecho in trechos:
            if (len(trecho.text) > 20): #Necessario por alguns jornalistas da globo fazem uso indevido da classe text__container para escrever substitulo
            #print(trecho.text)
            #print(len(trecho.text), "\n")
                ret += " " 
                ret+= (trecho.text)
        return ret

    def get_subtitle(self):
        return self.currentWrapper.find_element(*self.subtitle_locator).text
        
    
    def get_title(self):
        return self.currentWrapper.find_element(*self.title_locator).text
        

    def get_author(self):
        return self.currentWrapper.find_element(*self.author_locator).get_attribute('title')

    def get_category(self, articleUrl):
        #time.sleep(2)
        return articleUrl.split('/noticia/')[0].split('.com/')[1].replace('/' , '-')
        #return self.currentWrapper.find_element(*self.category_locator).text

    
    def get_main_wrapper(self, articleUrl):
        self.currentWrapper = self.driver.find_element(*self.main_wrapper_locator)

    def get_date(self):
        return self.currentWrapper.find_element(*self.date_locator).text
        pass
    
    def get_main_video_url(self):
        block0 = self.currentWrapper.find_element(By.XPATH , '//div[@data-block-id="0"]')

        if (block0.get_attribute('data-block-type') == 'backstage-video'):
            return "globoplay.globo.com/v/" + block0.find_element(*self.video_locator).get_attribute('data-video-id') 
        else:
            return "NULL"
        pass

    def get_main_image_url(self):
        block0 = self.currentWrapper.find_element(By.XPATH , '//div[@data-block-id="0"]')

        if (block0.get_attribute('data-block-type') == 'backstage-photo'):
            return block0.find_element(*self.image_locator).get_attribute('src') 
        else:
            return "NULL"

        #images = []
        #images = self.currentWrapper.find_elements(*self.image_locator)
        #return images[0].get_attribute('src')
        #for image in images:




    def scrap_article(self, articleUrl):
        self.access_article(articleUrl)
        time.sleep(2)
        self.get_main_wrapper(articleUrl)

        features = dict()
        features['Titulo'] = self.get_title()
        features['Subtitulo'] = self.get_subtitle()
        features['Data'] = self.get_date()
        features['URL'] = articleUrl
        features['Fonte'] = self.fonte
        features['Texto'] = self.get_text()
        features['Imagem'] = self.get_main_image_url()
        #features['Texto']
        features['Video'] = self.get_main_video_url()
        features['Autor'] = self.get_author()
        features['Categoria'] = self.get_category(articleUrl)
        features['Tipo'] = self.type
        
        print(features)

G1 = G1Scrapper(0)
#Video no topo
#G1.scrap_article("https://g1.globo.com/bemestar/coronavirus/noticia/2021/04/25/covid-19-ja-matou-mais-brasileiros-em-4-meses-de-2021-do-que-em-todo-ano-de-2020.ghtml")

#Imagem no topo
G1.scrap_article("https://g1.globo.com/ciencia-e-saude/noticia/2020/02/03/chineses-que-sairam-de-cidade-em-quarentena-por-coronavirus-pedem-a-quem-ficou-para-cuidar-de-animais-de-estimacao.ghtml")

#Sem nada
#G1.scrap_article("https://g1.globo.com/bemestar/vacina/noticia/2021/04/25/brasil-aplicou-ao-menos-uma-dose-de-vacina-contra-covid-em-mais-de-29-milhoes-de-pessoas-aponta-consorcio-de-veiculos-de-imprensa.ghtml") 
