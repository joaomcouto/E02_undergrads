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

class EfarsasScrapper(BaseCrawler):
    def __init__(self,interface):
        if interface:
            super(EfarsasScrapper, self).__init__("firefox")
        else:
            super(EfarsasScrapper, self).__init__()

        self.text_locator = (By.CLASS_NAME,'td_block_wrap.tdb_single_content.tdi_98.td-pb-border-top.td_block_template_1.td-post-content.tagdiv-type')
       # self.subtitle_locator = (By.CLASS_NAME,'content-head__subtitle')
        self.title_locator =(By.CLASS_NAME,'tdb-title-text')
        self.image_locator = (By.CLASS_NAME,'td_block_wrap.tdb_single_featured_image.tdi_97.tdb-content-horiz-left.td-pb-border-top.td_block_template_1')
        self.author_locator =  (By.CLASS_NAME , 'tdb-author-name-wrap')
        self.category_locator = (By.CLASS_NAME,'tdb-entry-category')
        self.veredict_locator = (By.CLASS_NAME,'tdb-entry-category')
        self.main_wrapper_locator = (By.ID, 'tdi_59')
        self.date_locator = (By.CLASS_NAME, 'td_block_wrap.tdb_single_date.tdi_72.td-pb-border-top.td_block_template_1.tdb-post-meta')
        self.type = "checagem"
        self.fonte = "e-farsas"
        #self.video_locator = (By.CLASS_NAME, "content-video__placeholder")

    def access_article(self, articleUrl):
        self.driver.get(articleUrl)

    def get_text(self):
        ret = ""
        texto = self.currentWrapper.find_element(*self.text_locator)
        trechos = texto.find_elements(By.TAG_NAME, 'p') 
        for trecho in trechos:
            if (len(trecho.text) > 20):
                ret += trecho.text
                ret += " "
        return ret
    

    def get_subtitle(self):
        return "NULL"
        
    
    def get_title(self):
        return self.currentWrapper.find_element(*self.title_locator).text
        

    def get_author(self):
        return self.currentWrapper.find_element(*self.author_locator).find_element(By.CLASS_NAME, 'tdb-author-name').text

    def get_category(self, articleUrl):
        categories = []
        allCategories = self.currentWrapper.find_elements(*self.category_locator)
        for cat in allCategories:
            if cat.text.lower() not in ['verdadeiro', 'falso']:
                categories.append(cat.text.lower())
        return categories

    def get_veredict(self):
        allCategories = self.currentWrapper.find_elements(*self.category_locator)
        for cat in allCategories:
            if cat.text.lower() in ['verdadeiro', 'falso']:
                return cat.text.lower()

    
    def get_main_wrapper(self, articleUrl):
        self.currentWrapper = self.driver.find_element(*self.main_wrapper_locator)

    def get_date(self):
        return self.currentWrapper.find_element(*self.date_locator).text

    
    def get_main_video_url(self):
        return "NULL"

    def get_main_image_url(self):
        return self.currentWrapper.find_element(*self.image_locator).find_element(By.TAG_NAME, 'img').get_attribute('src') 

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
        ##features['Texto']
        features['Video'] = self.get_main_video_url()
        features['Veredito'] = self.get_veredict()
        features['Autor'] = self.get_author()
        features['Categoria'] = self.get_category(articleUrl)
        features['Tipo'] = self.type
        
        print(features)

e = EfarsasScrapper(0)
e.scrap_article("https://www.e-farsas.com/cachorro-se-teletransporta-para-nao-ser-atropelado.html")
e.driver.quit()
