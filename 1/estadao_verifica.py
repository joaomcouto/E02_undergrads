from selenium import webdriver
import datetime
import time
from selenium.webdriver.support.ui import WebDriverWait       
from selenium.webdriver.common.by import By       
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

class Estadao_Verifica():

	def __init__(self):
		self.text_locator = (By.CLASS_NAME,'n--noticia__content')
		self.title_locator = 'data-titulo' #(By.CLASS_NAME,'n--noticia__title')
		#self.category_locator = não tem, somente o editorial Politica/eleições
		self.author_locator = "data-credito"
		self.date_locator = (By.CLASS_NAME,"n--noticia__state")
		self.image_locator = (By.TAG_NAME,'img')
		#self.verdict_locator = ?
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
			
	def scrapper(self, url):
		infos = {'Titulo':'',
			'Data':'',
			'Autor':'',
			'Texto':'',
			'Imagem':'',
			'Veredito':'',
			'Url':'',
			'Html':''}
		driver = webdriver.Firefox()
		driver.get(url)
		wrapper = driver.find_element(*self.wrapper_locator)
		date = wrapper.find_element(*self.date_locator).text
		infos['Data'] = self.convert_date(date)
		infos['Titulo'] = wrapper.get_attribute(self.title_locator)
		infos['Autor']  = self.author_extract(wrapper.get_attribute(self.author_locator))
		infos['Texto']  = wrapper.find_element(*self.text_locator).text
		infos['Imagem'] = wrapper.find_element(*self.image_locator).get_attribute('src')
		infos['Url']    = driver.current_url
		infos["Html"] = driver.page_source
		driver.close()
		return infos




EV =  Estadao_Verifica()
u_1_comma  = 'https://politica.estadao.com.br/blogs/estadao-verifica/e-falso-que-ex-apresentador-tenha-vazado-diretrizes-da-globo-para-criticar-bolsonaro/'
u_m_author = 'https://politica.estadao.com.br/blogs/estadao-verifica/em-discurso-na-cupula-do-clima-bolsonaro-distorce-dados-sobre-preservacao-ambiental/'
u_1_author = 'https://politica.estadao.com.br/blogs/estadao-verifica/requisicao-de-ambulancias-pelo-governo-da-bahia-esta-previsto-na-constituicao/'
u_2_author = 'https://politica.estadao.com.br/blogs/estadao-verifica/e-falso-que-tv-tenha-simulado-enterro-para-causar-panico-no-espirito-santo/'
u_sus = 'https://politica.estadao.com.br/blogs/estadao-verifica/video-de-lula-e-editado-para-parecer-que-ex-presidente-comemorou-bebado-decisao-de-fachin/'
d = EV.scrapper(u_sus) 
print(d)
