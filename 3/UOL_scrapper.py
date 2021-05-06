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

class UOLScrapper(BaseCrawler):
    def __init__(self,interface):
        if interface:
            super(UOLScrapper, self).__init__("firefox")
        else:
            super(UOLScrapper, self).__init__()

        self.text_locator = (By.CLASS_NAME,'text')
        #self.subtitle_locator = (By.CLASS_NAME,'content-head__subtitle')
        self.title_locator =(By.CLASS_NAME,'col-sm-22.col-md-22.col-lg-22.custom-title')
        self.image_locator = (By.CLASS_NAME,'pinit-wraper')
        self.author_locator =  (By.CLASS_NAME , 'p-author-local')
        self.category_locator =(By.CLASS_NAME,'title-name')
        self.main_wrapper_locator = (By.CLASS_NAME, 'article.article-wrapper.scroll-base.clearfix.collection-item.collection-first-item')
        self.date_locator = (By.CLASS_NAME, 'p-author.time')
        self.type = "noticia"
        self.fonte = "UOL"
        #self.video_locator = (By.CLASS_NAME, "content-video__placeholder")



    def access_article(self, articleUrl):
        self.driver.get(articleUrl)

    def get_text(self):
        ret = ""
        texto = self.currentWrapper.find_element(*self.text_locator)
        trechos = texto.find_elements(By.TAG_NAME, 'p')
        for trecho in trechos:
            if (len(trecho.text) > 20):  #Necessario para reduzir chances de captar lixo
                try:
                    trecho.find_element(By.TAG_NAME, 'cite')
                    ret+= '"'
                    ret+= (trecho.text)
                    #ret+= '"' #Jornalistas ja botam a segunda quote
                    ret+= " " 
                except:
                    ret+= (trecho.text)
                    ret+= " " 
                #print(trecho.text)
                #print(len(trecho.text), "\n")
                
            
        return ret

    def get_subtitle(self):
        return "NULL"
        #return self.currentWrapper.find_element(*self.subtitle_locator).text
        
    
    def get_title(self):
        return self.currentWrapper.find_element(*self.title_locator).text
        

    def get_author(self):
        return self.currentWrapper.find_element(*self.author_locator).text

    def get_category(self, articleUrl):
        #time.sleep(2)
        return articleUrl.split('.br/')[1].split('/')[0]
        #return self.currentWrapper.find_element(*self.category_locator).text

    
    def get_main_wrapper(self, articleUrl):
        self.currentWrapper = self.driver.find_element(*self.main_wrapper_locator)

    def get_date(self):
        ret = self.currentWrapper.find_element(*self.date_locator).text
        index = ret.find("Atu")
        ret = ret[:index] + " " + ret[index:]
        return ret
  
    def get_main_video_url(self):
        return "NULL"
    #    block0 = self.currentWrapper.find_element(By.XPATH , '//div[@data-block-id="0"]')

        #if (block0.get_attribute('data-block-type') == 'backstage-video'):
         #   return "globoplay.globo.com/v/" + block0.find_element(*self.video_locator).get_attribute('data-video-id') 
        #else:
        #    return "NULL"
        #pass

    def get_main_image_url(self):
        img = self.currentWrapper.find_element(*self.image_locator)
        return img.find_element(By.TAG_NAME,'img').get_attribute('src')

   #     block0 = self.currentWrapper.find_element(By.XPATH , '//div[@data-block-id="0"]')

    #    if (block0.get_attribute('data-block-type') == 'backstage-photo'):
     #       return block0.find_element(*self.image_locator).get_attribute('src') 
     #   else:
      #      return "NULL"

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
        features['Video'] = self.get_main_video_url()
        features['Autor'] = self.get_author()
        features['Categoria'] = self.get_category(articleUrl)
        features['Tipo'] = self.type
        
        print(features)

u = UOLScrapper(0)
#Video no topo
#G1.scrap_article("https://g1.globo.com/bemestar/coronavirus/noticia/2021/04/25/covid-19-ja-matou-mais-brasileiros-em-4-meses-de-2021-do-que-em-todo-ano-de-2020.ghtml")

#Imagem no topo
u.scrap_article("https://noticias.uol.com.br/saude/ultimas-noticias/redacao/2021/05/03/3-onda-covid-sp-edson-aparecido.htm")

#Sem nada
#G1.scrap_article("https://g1.globo.com/bemestar/vacina/noticia/2021/04/25/brasil-aplicou-ao-menos-uma-dose-de-vacina-contra-covid-em-mais-de-29-milhoes-de-pessoas-aponta-consorcio-de-veiculos-de-imprensa.ghtml") 