from selenium import webdriver
import datetime
import time
import json
import os
import hashlib
from selenium.webdriver.support.ui import WebDriverWait       
from selenium.webdriver.common.by import By       
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

"""
EXTRATOR DE VEREDITOS: 
	Tenta extrair a partir da imagem da thumb da checagem um dos 3
	vereditos possiveis(falso,enganoso ou fora de contexto). Utiliza
	modulos de OCR para Python (Pytesseract)

# import io
# import requests
# import pytesseract
# from PIL import Image

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
"""
def file_name(url):
    value = new_hash = hashlib.sha1(url.encode()).hexdigest()
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
		self.agency = 'estadao_verifica'
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
			return (text.strip()).split(',')
	
	def filter_links(self, links_list):		
			if len(filter_links) < 0:
				for link in links_list:
					if ('crop/117x66' not in link) or ('/117x66/' not in link):
						return link
			else:
				return 'NULL'	
			
	def scrapper(self, url):
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

		# tag_list = []
		# url,img_link = links.split(',')
		# url = url[2:-2]
		# img_link = img_link[2:-2]

		driver = webdriver.Firefox()
		driver.get(url)
		#infos['rating'] = extract_text_from_image(img_link)
		wrapper = driver.find_element(*self.wrapper_locator)
		date = wrapper.find_element(*self.date_locator).text
		infos['publication_date'] = self.convert_date(date)
		infos['title']       = wrapper.get_attribute(self.title_locator)
		try:
			infos['subtitle']    = wrapper.find_element(*self.subtitle_locator).text
		except:
			infos['subtitle'] = 'NULL'	
		infos['authors']     = self.author_extract(wrapper.get_attribute(self.author_locator))
		text_obj = wrapper.find_element(*self.text_locator)
		infos['text_news']   = text_obj.text
		infos['url']         = driver.current_url
		infos['obtained_at'] = datetime.date.today().strftime('%Y-%m-%d %H:%M:%S')

		try:
			img_objs  = text_obj.find_elements(*self.image_locator)
			for img in img_objs:
				link = img.get_attribute('src')
				img_links.append(link)
			infos['image_link'] = self.filter_links(img_links)
		except:
			infos['image_link'] = 'NULL'



		#Extrair tags
		try:
			tag_list = []
			tags = wrapper.find_elements(*self.tags_locator)
			for tag in tags:
				tag_list.append(tag.text)
			infos['tags'] = tag_list
		except NoSuchElementException:
			infos['tags'] = tag_list
			print("Não possui tags")

		#Nomear e salvar HTML da checagem
		value = hashlib.sha1(url.encode()).hexdigest()
		file_path = 'COLETORES/IMPLEMENTADOS/CHECAGENS/ESTADAO_VERIFICA/HTML/'+value+'.html'
		with open(file_path,'w') as file:
			file.write(driver.page_source)
		infos["raw_file_name"] = value

		driver.close()
		return infos

	def saving(self,dict_data):
		date = dict_data['publication_date']
		date = date.split('-')
		year = date[0]
		month = date[1]
		file_path = 'COLETORES/IMPLEMENTADOS/CHECAGENS/ESTADAO_VERIFICA/COLETA/estadao_verifica_'+year+'_'+month+'.txt'		
		with open(file_path, mode='a', encoding='utf-8') as f:
			f.write(json.dumps(dict_data, ensure_ascii=False) + '\n')

	def scrap_check(self,url):
		try:
			D = self.scrapper(url)
			try:
				self.saving(D)
				print('Página Coletada!')
			except Exception as S:
				print('Ocorreu um erro no salvamento!\n Erro: ', S)
		except Exception as E:
			print('Ocorreu um erro na coleta!\n Erro: ', E)
			return


	def execute(self):
		file_path = 'URLS/urls_'+self.agency+'.txt'
		with open(file_path,'r') as file:
			for line in file:
				data = json.loads(line)
				try:
					D = self.scrapper(data['url'])
					self.saving(D)
					print('Pagina coletada!')
				except Exception as ex:
					with open('exceptions_estadao.txt','a') as except_file:
						except_file.write(data['url']+' -'+str(ex)+'-\n')
