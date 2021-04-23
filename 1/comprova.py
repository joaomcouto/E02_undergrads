from selenium import webdriver
import datetime
import time
from selenium.webdriver.support.ui import WebDriverWait       
from selenium.webdriver.common.by import By       
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException


class Comprova():
	def __init__(self):
		#self.text_locator = 
		self.title_locator =(By.CLASS_NAME,'answer__title')
		self.image_locator = (By.TAG_NAME,'img')
		#self.author_locator =  não tem
		self.category_locator =(By.CLASS_NAME,'answer__term')
		self.verdict_locator = (By.CLASS_NAME,'answer__tag')
		self.main_wrapper_locator = (By.CLASS_NAME, 'site-main')
	def crawl_info(self,url):
		driver = webdriver.Firefox()
		infos = {'Titulo' : '', 
				'Texto': '',
				'Categoria':'',
				'Imagem':'',
				'Veredito':'',
				'Html':''}
		driver.get(url.strip())
		wrapper = driver.find_element(*self.main_wrapper_locator)
		category = wrapper.find_element(*self.category_locator).text
		title = wrapper.find_element(*self.title_locator).text
		image = wrapper.find_element(*self.image_locator).get_attribute('src')
		verdict = wrapper.find_element(*self.verdict_locator).text
		#text = 
		infos['Titulo'] = title
		#infos["Texto"]  = text  
		infos['Categoria'] = category
		infos['Imagem'] = image
		infos['Veredito'] = verdict
		#infos['Html'] = driver.page_source
		driver.close()
		return infos

C = Comprova()
u = 'https://projetocomprova.com.br/publica%C3%A7%C3%B5es/video-deturpa-informacoes-sobre-a-atuacao-do-governo-na-preservacao-da-amazonia/'
d = C.crawl_info(u)
print(d)


