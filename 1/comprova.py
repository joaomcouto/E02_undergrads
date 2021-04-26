from selenium import webdriver
import datetime
import time
from selenium.webdriver.support.ui import WebDriverWait       
from selenium.webdriver.common.by import By       
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException


class Comprova():
	def __init__(self):
		self.text_locator = (By.CSS_SELECTOR,'.answer__content--main')
		self.header_text_locator = (By.CLASS_NAME,'answer__tag__details')
		self.title_locator =(By.CLASS_NAME,'answer__title')
		self.image_locator = (By.TAG_NAME,'img')
		self.button_locator = (By.CLASS_NAME, 'answer__content__expand__label')
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
		button = WebDriverWait(driver, 30).until(EC.presence_of_element_located(self.button_locator))
		driver.execute_script("arguments[0].click();", button)
		time.sleep(1)
		main_txt = wrapper.find_element(*self.text_locator).text
	

		infos['Titulo'] = wrapper.find_element(*self.title_locator).text
		infos["Texto"]  = wrapper.find_element(*self.header_text_locator).text +'\n'+ main_txt
		infos['Categoria'] = wrapper.find_element(*self.category_locator).text
		infos['Imagem'] = wrapper.find_element(*self.image_locator).get_attribute('src')
		infos['Veredito'] = wrapper.find_element(*self.verdict_locator).text
		#infos['Html'] = driver.page_source
		driver.close()
		return infos

C = Comprova()
u = 'https://projetocomprova.com.br/publica%C3%A7%C3%B5es/video-deturpa-informacoes-sobre-a-atuacao-do-governo-na-preservacao-da-amazonia/'
#u2 = 'https://projetocomprova.com.br/publica%C3%A7%C3%B5es/media-de-mortes-em-2020-nao-foi-menor-que-em-2019/'
d = C.crawl_info(u)
print(d)


