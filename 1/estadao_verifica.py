from selenium import webdriver
import datetime
import time
import json
import os
from selenium.webdriver.support.ui import WebDriverWait       
from selenium.webdriver.common.by import By       
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException


import io
import requests
import pytesseract
from PIL import Image

def extract_text_from_image(image_link):
    #inFile = Image.open(image_name)
    #text = pytesseract.image_to_string(inFile, lang='eng')

    response = requests.get(image_link)
    img = Image.open(io.BytesIO(response.content))
    
    box_cntx1 = (181,67,322,133) #usar falso2 para pegar 'fora de'
    box_cntx2 = (164,61,314,120)
    box_falso1 = (218,87,325,117)
    box_falso2 = (182,62,322,103)
    box_enganoso1 = (163,84,330,121)
    box_enganoso2 = (150,57,311,86)
    
    crop1 = img.crop(box_falso1)
    crop2 = img.crop(box_falso2)
    text1 = pytesseract.image_to_string(crop1)
    text2 = pytesseract.image_to_string(crop2)
    #print('1 -> ',text1.strip(),'2 ->', text2.strip())
    if ("FALSO" in text1) or ("FALSO" in text2):
        return ["FALSO"]
    elif ("FORA" in text2):
        return ["FORA DE CONTEXTO"]
    else:
        crop1 = img.crop(box_cntx1)
        crop2 = img.crop(box_cntx2)
        text1 = pytesseract.image_to_string(crop1)
        text2 = pytesseract.image_to_string(crop2)
        #print('1 -> ',text1.strip(),'2 ->', text2.strip())
        if ("FORA" in text1) or ("FORA" in text2) or ("CONTEXTO" in text1) or ("CONTEXTO" in text2):
            return ["FORA DE CONTEXTO"]
        else:
            crop1 = img.crop(box_enganoso1)
            crop2 = img.crop(box_enganoso2)
            text1 = pytesseract.image_to_string(crop1)
            text2 = pytesseract.image_to_string(crop2)
            #print('1 -> ',text1.strip(),'2 ->', text2.strip())
            if ("ENGANOSO" in text1 ) or ("ENGANOSO" in text2):
                return ["ENGANOSO"]
            else:
                return ["None"]

def file_name(url):
    value = hash(url)
    if value < 0:
        name = '0' + str(abs(value)) + '.html'
    else:
        name = str(value) + '.html'
    return name

class Estadao_Verifica():

	def __init__(self):
		self.text_locator = (By.CLASS_NAME,'n--noticia__content')
		self.title_locator = 'data-titulo' #(By.CLASS_NAME,'n--noticia__title')
		#self.category_locator = não tem, somente o editorial Politica/eleições
		self.author_locator = "data-credito"
		self.date_locator = (By.CLASS_NAME,"n--noticia__state")
		self.image_locator = (By.TAG_NAME,'img')
		self.subtitle_locator = (By.CLASS_NAME,'n--noticia__subtitle')
		self.wrapper_locator = (By.XPATH,"//section[contains(@class,'n--noticia')]")
		self.tags_locator = (By.CLASS_NAME,"n--noticias__tags__link")
	def month2num(self, month):
		if month == 'janeiro':
			return 1
		elif month == 'fevereiro':
			return 2
		elif month == 'março':
			return 3
		elif month == 'abril':
			return 4
		elif month == 'maio':
			return 5
		elif month == 'junho':
			return 6
		elif month == 'julho':
			return 7
		elif month == 'agosto':
			return 8
		elif month == 'setembro':
			return 9
		elif month == 'outubro':
			return 10
		elif month == 'novembro':
			return 11
		elif month == 'dezembro':
			return 12
		else:
			return 0
	
	def convert_date(self,text):
		s_text = text.split("\n")
		d_text = s_text[1].split("|")
		d_text = d_text[0].split(" ")
		d = int(d_text[0])
		m = self.month2num(d_text[2].strip())
		y = int(d_text[4])
		date_obj = datetime.date(y,m,d)
		return date_obj.strftime('%Y-%m-%d %H:%M:%S')

	def author_extract(self,text):
		if text.count(',') ==  0:
			if ' e ' in text:
				text = (text.strip()).split(' e ')
				return text
			text = (text.strip()).split(',')
			return text
		if text.count(',') == 1:
			if ' e ' and not 'especial'  in text:
				return text.strip()
			text = text.split(',')
			text = text[0]
			return (text.strip()).split(',')
		if text.count(',') > 1 :
			return (text.strip()).slipt(',')
			
	def scrapper(self, links):
		infos = {
		'url': '',
		'source_name':'ESTADAO_VERIFICA',
		'title': '',
		'subtitle': '',
		'publication_date': '',
		'text_news': '',
		'image_link': '',
		'video_link': '',
		'authors': [],
		'categories': [],
        'tags': [],
		'obtained_at': '',
		'rating': [],
		'raw_file_name': ''
		}
		tag_list = []
		url,img_link = links.split(',')
		url = url[2:-2]
		img_link = img_link[2:-2]

		driver = webdriver.Firefox()
		driver.get(url)
		infos['rating'] = extract_text_from_image(img_link)
		wrapper = driver.find_element(*self.wrapper_locator)
		date = wrapper.find_element(*self.date_locator).text
		infos['publication_date'] = self.convert_date(date)
		infos['title']       = wrapper.get_attribute(self.title_locator)
		infos['subtitle']    = wrapper.find_element(*self.subtitle_locator).text
		infos['authors']     = self.author_extract(wrapper.get_attribute(self.author_locator))
		infos['text_news']   = wrapper.find_element(*self.text_locator).text
		infos['image_link']  = wrapper.find_element(*self.image_locator).get_attribute('src')
		infos['url']         = driver.current_url
		infos['obtained_at'] = datetime.date.today().strftime('%Y-%m-%d %H:%M:%S')
		try:
			tags = wrapper.find_elements(*self.tags_locator)
			for tag in tags:
				tag_list.append(tag.text)
			infos['tags'] = tag_list
		except NoSuchElementException:
			infos['tags'] = tag_list
			print("Não possui tags")
		value = file_name(driver.current_url)
		file_path = 'ESTADAO_VERIFICA/HTML/'+value+'.html'
		with open(file_path,'w') as file:
			file.write(driver.page_source)
		infos["raw_file_name"] = file_path
		driver.close()
		return infos

	def saving(self,dict_data):
		date = d['publication_date']
		date = date.split('-')
		year = date[0]
		month = date[1]
		file_path = 'ESTADAO_VERIFICA/COLETA/estadao_verifica_'+year+'_'+month+'.txt'		
		with open(file_path, mode='a', encoding='utf-8') as f:
			f.write(json.dumps(dict_data, ensure_ascii=False) + '\n')

	def dict2json(self, d):
		print(d)
		date = d['publication_date']
		date = date.split('-')
		year = date[0]
		month = date[1]
		file_path = 'ESTADAO_VERIFICA/COLETA/estadao_verifica_'+year+'_'+month+'.txt'
		if os.path.exists(file_path):
			file = open(file_path,'a')
		else:
			file = open(file_path,'w')
		
		file.write(json.dumps(d) + '\n')
		file.close()

	def execute(self):
		file_path = 'Urls/urls_estadao_verifica.txt'
		file = (file_path, 'r')
		for line in file:
			D = scrapper(line)
			self.saving(D)
			print('Pagina coletada!')


EV =  Estadao_Verifica()
url ="('https://politica.estadao.com.br/blogs/estadao-verifica/para-inflar-manifestacoes-pro-bolsonaro-posts-tiram-de-contexto-reportagem-sobre-protesto-de-2015/', 'https://politica.estadao.com.br/blogs/crop/360x203/estadao-verifica/wp-content/uploads/sites/690/2021/05/copiadeestadao-verifica-cards3_020520213236.png')"
d = EV.scrapper(url)
EV.saving(d)
