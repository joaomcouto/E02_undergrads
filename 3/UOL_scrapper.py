import os
import env
import sys
import time
from datetime import datetime
import hashlib
import json

from news_crawler.base_crawler import BaseCrawler

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options

class UOLVideoException(Exception):
    pass

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
                try: #Necessario para conseguir identificar quotes e botar as aspas necessarias
                    trecho.find_element(By.TAG_NAME, 'cite')
                    ret+= '"'
                    ret+= (trecho.text)
                    #ret+= '"' #Jornalistas ja botam a segunda quote
                    ret+= " " 
                except:
                    ret+= (trecho.text)
                    ret+= " " 
        return ret

    def get_subtitle(self):
        return "NULL"

    def get_title(self):
        return self.currentWrapper.find_element(*self.title_locator).text
        

    def get_author(self):
        return self.currentWrapper.find_element(*self.author_locator).text

    def get_category(self, articleUrl):
        return [articleUrl.split('.br/')[1].split('/')[0]]

    def get_main_wrapper(self, articleUrl):
        self.currentWrapper = self.driver.find_element(*self.main_wrapper_locator)

    def get_date(self):
        rawDate = self.currentWrapper.find_element(*self.date_locator).text
        index = rawDate.find("Atu")
        rawDate, rawTime= rawDate[:index].split(" ")

        rawDay,rawMonth,rawYear = rawDate.split("/")
        rawHour, rawMinute = rawTime.split("h")

        data_publicacao = datetime( year=int(rawYear),
                                    month=int(rawMonth), 
                                    day=int(rawDay),
                                    hour=int(rawHour),
                                    minute=int(rawMinute))
        publication_date = data_publicacao.strftime('%Y-%m-%d %H:%M:%S')

        return publication_date 

    def get_main_video_url(self):
        return "NULL"

    def get_main_image_url(self):
        img = self.currentWrapper.find_element(*self.image_locator)
        return img.find_element(By.TAG_NAME,'img').get_attribute('src')

    def scrap_article(self, articleUrl):
        if("/video" in articleUrl):
            raise UOLVideoException("Artigos 'video' do UOL são apenas links para o YT deles, não coletaremos. Trate essa excessão para dar continuidade à coleta!")
        self.access_article(articleUrl)
        time.sleep(2)
        self.get_main_wrapper(articleUrl)

        features = dict()
        features['url'] = articleUrl
        features['source_name'] = self.fonte
        features['title'] = self.get_title()
        features['subtitle'] = self.get_subtitle()
        
        features['publication_date'] = self.get_date()
        
        
        features['text_news'] = self.get_text()
        features['image_link'] = self.get_main_image_url()
        features['video_link'] = self.get_main_video_url()
        features['authors'] = self.get_author()
        features['categories'] = self.get_category(articleUrl)

        features['obtained_at'] = datetime.today().strftime('%Y-%m-%d %H:%M:%S')

        features['raw_file_name'] = self.html_file_name(articleUrl)
        self.save_html(features)

        return features

    def append_article_to_txt(self, features):
        file_path = os.getenv('PROJECT_DIR') + "/UOL/COLETA/" + features['source_name'].lower() + "_" + '_'.join(features['publication_date'].split('-')[0:2]) + ".txt"
        with open(file_path, mode='a', encoding='utf-8') as f:
            f.write(json.dumps(features, ensure_ascii=False) + '\n')
    
    def html_file_name(self,url):
        return hashlib.sha1(url.encode()).hexdigest()+ ".html"

    def save_html(self, features):
        file_path = os.getenv('PROJECT_DIR') + "/UOL/HTML/" + features['raw_file_name'] 
        with open(file_path, mode='w', encoding='utf-8') as f:
            f.write(self.driver.page_source)

u = UOLScrapper(0)
try:
    data = u.scrap_article("https://noticias.uol.com.br/politica/ultimas-noticias/2021/05/22/aziz-bolsonaro-queria-que-eu-prendesse-wajngarten-e-acabasse-a-cpi.htm")
except UOLVideoException:
    print("Artigos 'video' do UOL são apenas links para o YT deles, não coletaremos.")
else:    
    u.append_article_to_txt(data)
finally:
    u.driver.close()
    u.driver.quit()
