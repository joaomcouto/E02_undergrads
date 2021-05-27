import os
import env
import sys
import time
import json
import hashlib
import logging
from datetime import datetime

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
        try:
            return self.currentWrapper.find_element(*self.subtitle_locator).text
        except:
            return "NULL"
        
    def get_title(self):
        return self.currentWrapper.find_element(*self.title_locator).text
        
    def get_author(self):
        try:
            return self.currentWrapper.find_element(*self.author_locator).get_attribute('title')
        except:
            return "NULL"

    def get_category(self, articleUrl):
        return articleUrl.split('/noticia/')[0].split('.com/')[1].split('/')#replace('/' , '-')

    def get_main_wrapper(self, articleUrl):
        self.currentWrapper = self.driver.find_element(*self.main_wrapper_locator)

    def get_date(self):
        #print()self.currentWrapper.find_element(*self.date_locator).text.split(" ")
        rawDate,rawTime = self.currentWrapper.find_element(*self.date_locator).text.split(" ")
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

    def scrap_article(self, articleUrl):
        self.access_article(articleUrl)
       # time.sleep(3)
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
        file_path = os.getenv('DATA_DIR') + "/G1/COLETA/" + features['source_name'].lower() + "_" + '_'.join(features['publication_date'].split('-')[0:2]) + ".txt"
        with open(file_path, mode='a', encoding='utf-8') as f:
            f.write(json.dumps(features, ensure_ascii=False) + '\n')
    
    def html_file_name(self,url):
        return hashlib.sha1(url.encode()).hexdigest()+ ".html"

    def save_html(self, features):
        file_path = os.getenv('DATA_DIR') + "/G1/HTML/" + features['raw_file_name'] 
        with open(file_path, mode='w', encoding='utf-8') as f:
            f.write(self.driver.page_source)

    def scrap_urls_file(self, fileName, taskName):
        LOG_FILENAME = os.getenv('DATA_DIR') + '/G1/LOG/' + taskName + '.log'
        logging.basicConfig(filename=LOG_FILENAME, filemode ='w',level=logging.ERROR)
        
        with open(fileName) as f:
            for url in f:
                retry = 3
                while(retry > 0):
                    try:
                        data = self.scrap_article(url)
                        self.append_article_to_txt(data)
                        retry = 3
                        break
                    except Exception as e:
                        retry = retry - 1
                        if retry ==0:
                            logging.exception(url)
        self.driver.close()
                    

start = time.time()
G1 = G1Scrapper(0)
G1.scrap_urls_file('G1/URL/G1_bemestar_coronavirus_historica_may_24.txt','historica')
print("Total elapsed time:", time.time() -start)
G1.driver.quit()

        
        
#G1 = G1Scrapper(0)
#Video no topo
#data = G1.scrap_article("https://g1.globo.com/bemestar/coronavirus/noticia/2021/04/25/covid-19-ja-matou-mais-brasileiros-em-4-meses-de-2021-do-que-em-todo-ano-de-2020.ghtml")
#G1.append_article_to_txt(data)

#Imagem no topo
#G1.scrap_article("https://g1.globo.com/ciencia-e-saude/noticia/2020/02/03/chineses-que-sairam-de-cidade-em-quarentena-por-coronavirus-pedem-a-quem-ficou-para-cuidar-de-animais-de-estimacao.ghtml")

#Sem nada
#data = G1.scrap_article("https://g1.globo.com/bemestar/vacina/noticia/2021/04/25/brasil-aplicou-ao-menos-uma-dose-de-vacina-contra-covid-em-mais-de-29-milhoes-de-pessoas-aponta-consorcio-de-veiculos-de-imprensa.ghtml")
#G1.append_article_to_txt(data)
#G1.scrap_article("") 

#data = G1.scrap_article("https://g1.globo.com/bemestar/coronavirus/noticia/2021/05/21/numero-de-mortes-na-pandemia-pode-ser-ate-tres-vezes-maior-do-que-o-registrado-aponta-relatorio-da-oms.ghtml")
#G1.append_article_to_txt(data)
#G1.driver.close()

