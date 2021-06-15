import os
import env
import sys
import time
import json
import hashlib
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
        self.tags_locator = (By.CLASS_NAME, 'tdb-tags')
        self.type = "checagem"
        self.fonte = "efarsas"
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
        return [self.currentWrapper.find_element(*self.author_locator).find_element(By.CLASS_NAME, 'tdb-author-name').text]

    def get_category(self):
        categories = []
        allCategories = self.currentWrapper.find_elements(*self.category_locator)
        for cat in allCategories:
            if cat.text.lower() not in ['verdadeiro', 'falso']:
                categories.append(cat.text.lower())
        return categories

    def get_tags(self):
        tags = []
        tagsElement = self.currentWrapper.find_element(*self.tags_locator)
        allTags = tagsElement.find_elements(By.TAG_NAME, 'li')
        for tag in allTags:
            if tag.text.lower() not in ['tags']:
                tags.append(tag.text.lower())
        return tags

    def get_veredict(self):
        allCategories = self.currentWrapper.find_elements(*self.category_locator)
        for cat in allCategories:
            if cat.text.lower() in ['verdadeiro', 'falso']:
                return [cat.text.lower()]

    def get_main_wrapper(self, articleUrl):
        self.currentWrapper = self.driver.find_element(*self.main_wrapper_locator)

    def get_date(self):
        rawDate = self.currentWrapper.find_element(*self.date_locator).text
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
        rawDay,rawMonth,rawYear = rawDate.split(" de ")
        rawMonth = mapper[rawMonth.lower()]

        data_publicacao = datetime( year=int(rawYear),
                                    month=int(rawMonth), 
                                    day=int(rawDay))
        publication_date = data_publicacao.strftime('%Y-%m-%d %H:%M:%S')

        return publication_date 
    
    def get_main_video_url(self):
        return "NULL"

    def get_main_image_url(self):
        return self.currentWrapper.find_element(*self.image_locator).find_element(By.TAG_NAME, 'img').get_attribute('src') 

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
        features['categories'] = self.get_category()
        features['tags'] = self.get_tags()
        features['obtained_at'] = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        features['rating'] = self.get_veredict()
        features['raw_file_name'] = self.html_file_name(articleUrl)
        self.save_html(features)
        return features

    def append_article_to_txt(self, features):
        file_path = os.getenv('PROJECT_DIR') + "/EFARSAS/COLETA/" + features['source_name'].lower() + "_" + '_'.join(features['publication_date'].split('-')[0:2]) + ".txt"
        with open(file_path, mode='a', encoding='utf-8') as f:
            f.write(json.dumps(features, ensure_ascii=False) + '\n')
    
    def html_file_name(self,url):
        return hashlib.sha1(url.encode()).hexdigest()+ ".html"

    def save_html(self, features):
        file_path = os.getenv('PROJECT_DIR') + "/EFARSAS/HTML/" + features['raw_file_name'] 
        with open(file_path, mode='w', encoding='utf-8') as f:
            f.write(self.driver.page_source)

e = EfarsasScrapper(0)
data = e.scrap_article("https://www.e-farsas.com/cuba-adotou-com-sucesso-a-cloroquina-no-tratamento-de-pacientes-da-covid.html")
e.append_article_to_txt(data)
e.driver.quit()
