import os
import env
import sys
import time
import hashlib
import json
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

class BBCScrapper(BaseCrawler):
    def __init__(self,interface):
        if interface:
            super(BBCScrapper, self).__init__("firefox")
        else:
            super(BBCScrapper, self).__init__()

        self.text_locator = (By.CLASS_NAME,'bbc-19j92fr.e57qer20')
        #self.subtitle_locator = (By.CLASS_NAME,'content-head__subtitle') #BBC não tem subtitulo

        self.title_locator =(By.CLASS_NAME,'bbc-1lsgtu3.e1yj3cbb0')

        self.image_locator = (By.CLASS_NAME,'bbc-1qdcvv9.e6bmn90') #O difenrenciar da main image vai ser a nao presenca da classe lazyloader
        self.author_locator =  (By.CLASS_NAME , 'e1j2237y6.bbc-q4ibpr.e57qer20') #Algumas noticias na BBC nao tem autor

        #self.category_locator =(By.CLASS_NAME,'title-name') 
            #Noticias na BBC não tem categoria
            #Quase todas as noticiais sao 'geral' , 'internacional' ou 'brasil'
                # -> Coletarei isso da URL
            #Assim para saber a categoria DE VERDADE é necessario na hora do scrapping, ver de qual coleta de "editorial" a URL esta vindo
        

        self.main_wrapper_locator = (By.TAG_NAME, 'main')
        self.date_locator = (By.CLASS_NAME, 'e1j2237y7.bbc-q4ibpr.e57qer20')
        self.type = "noticia"
        self.fonte = "BBC"
        #self.video_locator = (By.CLASS_NAME, "content-video__placeholder") #BBC não tem vídeo 



    def access_article(self, articleUrl):
        self.driver.get(articleUrl)

    def get_text(self):
        ret = ""
        trechos = self.currentWrapper.find_elements(*self.text_locator)
                
        for trecho in trechos:
            #print("Trecho:", trecho.text , '\n')
            try: 
                #Necessario para jogar fora os substitulos ao longo da materia e tambem listagens para outras reportagens
                #Exemplo de materia com subtitulo e listagem: https://www.bbc.com/portuguese/geral-53681929
                para = trecho.find_element(By.TAG_NAME, 'p')

                if (len(para.text) > 15):  #Necessario para reduzir chances de captar lixo
                    if("Inscreva-se no nosso canal!" in para.text):
                        continue
                    ret+= (para.text)
                    ret+= " " 
                    #print(para.text)
                    #print(len(para.text), "\n")
            except:
                #print("Não tem a tag p, indicativo de substitulo, listagem ou propaganda do canal do BBC")
                continue
                
            
        return ret

    def get_subtitle(self):
        return "NULL"

    def get_title(self):
        return self.currentWrapper.find_element(*self.title_locator).text
        

    def get_author(self): #Algumas noticias na BBC nao tem autor vide https://www.bbc.com/portuguese/internacional-57143976
        try:
            return self.currentWrapper.find_element(*self.author_locator).text.replace('\n', ' ')
        except:
            return "NULL"

    def get_category(self, articleUrl):
        return [articleUrl.split('portuguese/')[1].split('-')[0]]
    
    def get_main_wrapper(self, articleUrl):
        self.currentWrapper = self.driver.find_element(*self.main_wrapper_locator)

    def get_date(self):
        rawDate = str(self.currentWrapper.find_element(*self.date_locator).text.split('\n')[0])
        mapper = {
                'janeiro': 1,
                'fevereiro': 2,
                'março': 3,
                'abril': 4,
                'maio': 5,
                'junho': 6,
                'julho': 7,
                'agosto': 8,
                'setembro': 9,
                'outubro': 10,
                'novembro': 11,
                'dezembro': 12
            }
        rawDay,rawMonth,rawYear = rawDate.split(" ")
        rawMonth = mapper[rawMonth]

        data_publicacao = datetime( year=int(rawYear),
                                    month=int(rawMonth), 
                                    day=int(rawDay))
        publication_date = data_publicacao.strftime('%Y-%m-%d %H:%M:%S')

        return publication_date 
  
    def get_main_video_url(self):
        return "NULL"

    def get_main_image_url(self):
        images = self.currentWrapper.find_elements(*self.image_locator)
        for im in images:       
            try: #Necessario para conseguir diferenciar a imagem principal de outras imagens na noticia
                im.find_element(By.CLASS_NAME, 'lazyload-wrapper')
            except:
                return im.find_element(By.TAG_NAME,'img').get_attribute('src')

    def scrap_article(self, articleUrl):
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
        file_path = os.getenv('PROJECT_DIR') + "/BBC/COLETA/" + features['source_name'].lower() + "_" + '_'.join(features['publication_date'].split('-')[0:2]) + ".txt"
        with open(file_path, mode='a', encoding='utf-8') as f:
            f.write(json.dumps(features, ensure_ascii=False) + '\n')
    
    def html_file_name(self,url):
        return hashlib.sha1(url.encode()).hexdigest()+ ".html"

    def save_html(self, features):
        file_path = os.getenv('PROJECT_DIR') + "/BBC/HTML/" + features['raw_file_name'] 
        with open(file_path, mode='w', encoding='utf-8') as f:
            f.write(self.driver.page_source)

b = BBCScrapper(0)
data = b.scrap_article("https://www.bbc.com/portuguese/internacional-57143976")
b.append_article_to_txt(data)
b.driver.close()



