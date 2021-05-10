from selenium import webdriver
import datetime
import time
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
        return "FALSO"
    elif ("FORA" in text2):
        return "FORA DE CONTEXTO"
    else:
        crop1 = img.crop(box_cntx1)
        crop2 = img.crop(box_cntx2)
        text1 = pytesseract.image_to_string(crop1)
        text2 = pytesseract.image_to_string(crop2)
        #print('1 -> ',text1.strip(),'2 ->', text2.strip())
        if ("FORA" in text1) or ("FORA" in text2) or ("CONTEXTO" in text1) or ("CONTEXTO" in text2):
            return "FORA DE CONTEXTO"
        else:
            crop1 = img.crop(box_enganoso1)
            crop2 = img.crop(box_enganoso2)
            text1 = pytesseract.image_to_string(crop1)
            text2 = pytesseract.image_to_string(crop2)
            #print('1 -> ',text1.strip(),'2 ->', text2.strip())
            if ("ENGANOSO" in text1 ) or ("ENGANOSO" in text2):
                return "ENGANOSO"
            else:
                return "None"


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
	def month2num(self, month):
		if month == 'janeiro':
			return '01'
		elif month == 'fevereiro':
			return '02'
		elif month == 'março':
			return '03'
		elif month == 'abril':
			return '04'
		elif month == 'maio':
			return '05'
		elif month == 'junho':
			return '06'
		elif month == 'julho':
			return '07'
		elif month == 'agosto':
			return '08'
		elif month == 'setembro':
			return '09'
		elif month == 'outubro':
			return '10'
		elif month == 'novembro':
			return '11'
		elif month == 'dezembro':
			return '12'
		else:
			return '00'
	def convert_date(self,text):
		s_text = text.split("\n")
		d_text = s_text[1].split("|")
		d_text = d_text[0].split(" ")
		d = d_text[0]
		m = self.month2num(d_text[2].strip())
		y = d_text[4]
		return (y+'-'+m+'-'+d)

	def author_extract(self,text):
		if text.count(',') ==  0:
			return text.strip()
		if text.count(',') == 1:
			if ' e ' and not 'especial'  in text:
				return text.strip()
			text = text.split(',')
			text = text[0]
			return text.strip()
		if text.count(',') > 1 :
			return text.strip()
			
	def scrapper(self, links):
		infos = {'Titulo':'',
			'Subtitulo': '',
			'Data':'',
			'Texto':'',
			'Imagem':'',
			'Video':'',
			'VideoChecagem':'',
			'Categorias':'',
			'Vereditos':'',
			'Url':'',
			'HTML':''}

		url,img_link = links.split(',')
		url = url[2:-2]
		img_link = img_link[2:-3]

		driver = webdriver.Firefox()
		driver.get(url)
		infos['Veredito'] = extract_text_from_image(img_link)  
		wrapper = driver.find_element(*self.wrapper_locator)
		date = wrapper.find_element(*self.date_locator).text
		infos['Data'] = self.convert_date(date)
		infos['Titulo'] = wrapper.get_attribute(self.title_locator)
		infos['Subtitulo'] = wrapper.find_element(*self.subtitle_locator).text
		infos['Autor']  = self.author_extract(wrapper.get_attribute(self.author_locator))
		infos['Texto']  = wrapper.find_element(*self.text_locator).text
		infos['Imagem'] = wrapper.find_element(*self.image_locator).get_attribute('src')
		infos['Url']    = driver.current_url
		infos["Html"] = driver.page_source
		driver.close()
		return infos



EV =  Estadao_Verifica()
