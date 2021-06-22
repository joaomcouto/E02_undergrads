from selenium import webdriver
import datetime
import time
import json
from selenium.webdriver.support.ui import WebDriverWait       
from selenium.webdriver.common.by import By       
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException


def file_name(url):
    value = new_hash = hashlib.sha1(url.encode()).hexdigest()
    if value < 0:
        name = '0' + str(abs(value)) + '.html'
    else:
        name = str(value) + '.html'
    return name

class Comprova():
	def __init__(self):
		self.text_locator = (By.CSS_SELECTOR,'.answer__content--main')
		self.header_text_locator = (By.CLASS_NAME,'answer__tag__details')
		self.title_locator =(By.CLASS_NAME,'answer__title')
		self.image_locator = (By.TAG_NAME,'img')
		self.button_locator = (By.CLASS_NAME, 'answer__content__expand__label')
		self.date_locator = (By.CLASS_NAME,'answer__credits__date')
		#self.author_locator =  não tem
		self.category_locator =(By.CLASS_NAME,'answer__term')
		self.verdict_locator = (By.CLASS_NAME,'answer__tag')
		self.main_wrapper_locator = (By.CLASS_NAME, 'site-main')
		self.agency = 'comprova'

	def saving(self,dict_data):
		date = dict_data['publication_date']
		date = date.split('-')
		year = date[0]
		month = date[1]
		file_path = 'COMPROVA/COLETA/comprova_'+year+'_'+month+'.txt'		
		with open(file_path, mode='a', encoding='utf-8') as f:
			f.write(json.dumps(dict_data, ensure_ascii=False) + '\n')

	def execute(self):
		file_path = 'URLS/urls_'+self.agency+'.txt'
		with open(file_path,'r') as file:
			for line in file:
				data = json.loads(line)
				try:
					D = self.scrapper(data['url'])
					self.saving(D)
					print('Pagina coletada!')
				except:
					with open('exeptions_comprova.txt','a') as except_file:
						except_file.write(data['url'] + '\n')


	def convert_date(self,text):
		date_text = text.split('-')
		d = int(date_text[2])
		m = int(date_text[1])
		y = int(date_text[0])
		date_obj = datetime.date(y,m,d)
		return date_obj.strftime('%Y-%m-%d %H:%M:%S')		

	def scrapper(self,url):
		driver = webdriver.Firefox()
		infos = {
		'url': '',
		'source_name':'COMPROVA',
		'title': '',
		'subtitle': '',
		'publication_date': '',
		'text_news': '',
		'image_link': '',
		'video_link': '',
		'authors': ['Projeto Comprova'],
		'categories': [],
        'tags': [],
		'obtained_at': '',
		'rating': [],
		'raw_file_name': ''
		}

		driver.get(url.strip())

		wrapper = driver.find_element(*self.main_wrapper_locator)
		button = WebDriverWait(driver, 30).until(EC.presence_of_element_located(self.button_locator))
		driver.execute_script("arguments[0].click();", button)
		time.sleep(1)
		main_txt = wrapper.find_element(*self.text_locator)
	

		infos['title'] = wrapper.find_element(*self.title_locator).text
		infos["text_news"]  = wrapper.find_element(*self.header_text_locator).text +'\n'+ main_txt.text
		infos['category'] = [wrapper.find_element(*self.category_locator).text]
		infos['rating'] = [wrapper.find_element(*self.verdict_locator).text]
		infos['url'] = driver.current_url
		infos['publication_date'] = self.convert_date(wrapper.find_element(*self.date_locator).text)
		infos['obtained_at'] = datetime.date.today().strftime('%Y-%m-%d %H:%M:%S')

		value = hashlib.sha1(url.encode()).hexdigest()
		file_path = 'COMPROVA/HTML/'+value+'.html'
		with open(file_path,'w') as file:
			file.write(driver.page_source)
		infos["raw_file_name"] = file_path

		try:
			infos['img_link'] = main_txt.find_element(*self.image_locator).get_attribute('src')
		except NoSuchElementException:
			infos['img_link'] = 'None'
		driver.close()
		return infos

C = Comprova()
C.execute()


