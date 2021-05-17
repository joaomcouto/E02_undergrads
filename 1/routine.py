#from news_crawler.base_crawler import BaseCrawler

from selenium import webdriver
import datetime
import time
from selenium.webdriver.support.ui import WebDriverWait       
from selenium.webdriver.common.by import By       
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException

def get_last_urls(agency):
	urls = []
	filename = "LAST_URL/last_" +agency+ ".txt"
	db = open(filename,"r")
	for line in db:
		urls.append(line)
	db.close()
	return urls[0]

def collect_all(Obj):
	urls = Obj.crawler_news(' ')
	file_path = "URLS/urls_"+Obj.agency+'.txt'
	file2_path = "LAST_URL/last_"+Obj.agency+'.txt'
	with open(file2_path,'w') as file2:
		file2.write(str(urls[0]))
	with open(file_path,'w') as file:
		for line in urls:
			file.write(str(line).strip()+'\n')


def write_routine(urls,agency):
	file_path = 'ROUTINES/routine_'+agency+'.txt'
	file2_path = 'LAST_URL/last_'+agency+'.txt'
	with open (file2_path,'w') as url_file:
		url_file.write(str(urls[0]))
	with open(file_path,'a') as routine_file:
		for line in urls:
			routine_file.write(str(line)+'\n')

class Lupa():
	def __init__(self):
		self.__baseUrl  = 'https://piaui.folha.uol.com.br/lupa'
		self.date_locator = (By.CLASS_NAME,"bloco-meta")
		self.button_locator = (By.CSS_SELECTOR,".btn-mais")
		self.news_locator = (By.CSS_SELECTOR,".internaPGN > div")
		self.agency = 'lupa'
		
	def convert_date(self,text_date):
		text_date = text_date.split(" | ")
		complete_date = text_date[0].split(".")
		day = int(complete_date[0])
		month = int(complete_date[1])
		year = int(complete_date[2])
		date  = datetime.date(year,month,day)
		return date
	
	def crawler_news(self,last_url):
		driver = webdriver.Firefox()
		driver.get(self.__baseUrl)
		url_list = []
				
		while True:
			news = driver.find_elements(*self.news_locator)
			for n in news:
				url = n.find_element_by_tag_name('a').get_attribute("href")
				if url == last_url:
					driver.close()
					return url_list
				url_list.append(url)
			try:
				time.sleep(1)
				button = driver.find_element(*self.button_locator)
				driver.get(button.get_attribute("href"))
			except NoSuchElementException:
				break
		driver.close()
		return url_list


	def execute_routine(self):
		urls = get_last_urls(self.agency)
		url = urls[0]
		url_news = self.crawler_news(url)
		write_routine(url_news,self.agency)
		return url_news

class Comprova(): 
	def __init__(self):
		self.__baseUrl  = 'https://projetocomprova.com.br/'
		self.date_locator = (By.CLASS_NAME,"answer__credits__date")
		self.pagination_locator = (By.CSS_SELECTOR,".pagination>a")
		self.news_locator = (By.TAG_NAME,'article')
		self.news_child_locator = (By.CLASS_NAME,"answer__title__link")
		self.agency = 'comprova'

	def convert_date(self,text_date):
		#exemple : 2021-03-05
		complete_date = text_date.split("-")
		date = datetime.date(int(complete_date[0]),int(complete_date[1]),int(complete_date[2]))
		return date
	def crawler_news(self,last_url):
		page_list = []
		url_list = []
		driver = webdriver.Firefox()
		driver.get(self.__baseUrl)
		pages = driver.find_elements(*self.pagination_locator)
		for p in pages:
			page_list.append(p.get_attribute("href"))
		for page_link in page_list:
			driver.get(page_link)
			news = driver.find_elements(*self.news_locator)
			for n in news:
				url = n.find_element(*self.news_child_locator).get_attribute("href")
				#raw_date = n.find_element_by_class_name(self.date_class).text
				#date = self.convert_date(raw_date)
				if url == last_url:
					driver.close()
					return url_list
				url_list.append(url)
				print(url)
		driver.close()
		return url_list

	def execute_routine(self):
		urls = get_last_urls(self.agency)
		url = urls[0]
		url_news = self.crawler_news(url)
		write_routine(url_news,self.agency)
		return url_news

class E_farsas():
	
	def __init__(self):
		self.__baseUrl = 'https://www.e-farsas.com/secoes/falso-2'
		self.wrapper_locator = (By.CSS_SELECTOR,'.tdi_78')
		self.mp_news_block_wrapper = (By.CSS_SELECTOR,'.tdi_83') #mp = MainPage
		self.mp_main_news_block_wrapper  =(By.CSS_SELECTOR,'.tdi_71')
		self.news_locator = (By.CLASS_NAME,'entry-title')
		self.button_locator = (By.XPATH,"//a[@aria-label='next-page']")
		self.agency = 'e_farsas'

	def execute_routine(self):
		urls = get_last_urls(self.agency)
		url = urls[0]
		url_news = self.crawler_news(url)
		write_routine(url_news,self.agency)
		return url_news

	def crawler_news(self,last_url):
		urls_list = []
		driver = webdriver.Firefox()
		driver.get(self.__baseUrl)
		IsMainPage  = True

		while True:
			if IsMainPage:
				block_wrapper = driver.find_element(*self.mp_main_news_block_wrapper)
				news = block_wrapper.find_elements(*self.news_locator)
				wrapper = driver.find_element(*self.mp_news_block_wrapper)
				mp_news = wrapper.find_elements(*self.news_locator)
				news.extend(mp_news)
			else:
				wrapper = WebDriverWait(driver, 30).until(EC.presence_of_element_located(self.wrapper_locator))
				news = wrapper.find_elements(*self.news_locator)
			
			for n in news:
				url = n.find_element_by_tag_name('a').get_attribute('href')
				if url == last_url:
					driver.close()
					return urls_list
				urls_list.append(url)
				print(url)
			try:
				button = driver.find_element(*self.button_locator)
				next_page = button.get_attribute('href')
				driver.get(next_page)
				IsMainPage = False
				time.sleep(0.5)
			except NoSuchElementException:
				break

		driver.close()
		return urls_list

class Boatos():
	
	def __init__(self):
		self.__baseUrl = 'https://www.boatos.org/contato'
		self.pagination_locator = (By.CSS_SELECTOR,'#archives-4 > ul:nth-child(2) > li')
		self.news_locator = (By.CLASS_NAME,"entry-title")
		self.date_class = (By.CLASS_NAME,'entry-date')
		self.button_locator = (By.CSS_SELECTOR,'.previous')
		self.agency = 'boatos'

	def execute_routine(self):
		urls = get_last_urls(self.agency)
		url = urls[0]
		url_news = self.crawler_news(url)
		write_routine(url_news,self.agency)
		return url_news

	def convert_date(self,text_date):
		pass
	def crawler_news(self,last_url):
		archive_list = []
		urls_list = []
		driver = webdriver.Firefox()
		driver.get(self.__baseUrl)

		archive = driver.find_elements(*self.pagination_locator)
		for ar in archive:
			ar_url = ar.find_element_by_tag_name("a").get_attribute("href")
			archive_list.append(ar_url)
		for page in archive_list:
			driver.get(page)
			while True:
				time.sleep(1)
				news = driver.find_elements(*self.news_locator)
				for n in news:
					url = n.find_element_by_tag_name("a").get_attribute("href")
					if url == last_url:
						driver.close()
						return urls_list
					urls_list.append(url)
				try:
					button = driver.find_element(*self.button_locator)
					next_page = button.find_element_by_tag_name("a").get_attribute("href")
					driver.get(next_page)
					time.sleep(1)
				except NoSuchElementException:
					break
		driver.close()
		return urls_list

class Aos_fatos():
	
	def __init__(self):
		self.__baseUrl = 'https://www.aosfatos.org/noticias/'
		self.news_locator = (By.CSS_SELECTOR,'.entry-card-list>a')
		self.button_locator = (By.CLASS_NAME,'next-arrow')
		self.category_locator = (By.CLASS_NAME,'entry-card-category')
		self.agency = 'aos_fatos'

	def execute_routine(self):
		urls = get_last_urls('aos_fatos')
		line = urls[0]
		routine_urls = self.crawler_news(line.strip())
		list_to_txt(routine_urls,'aos_fatos')
		return routine_urls

	def convert_date(self,text_date):
		pass
	def crawler_news(self,last_url):
		urls_list = []
		driver = webdriver.Firefox()
		driver.get(self.__baseUrl)
		while True:
			news = driver.find_elements(*self.news_locator)
			for n in news:
				url = n.get_attribute("href")
				category = n.find_element(*self.category_locator).text
				print(url,category)
				if url == last_url:
					driver.close()
					return urls_list
				urls_list.append((url,category))
			try:
				button = driver.find_element(*self.button_locator)
				next_page  = button.get_attribute("href")
				driver.get(next_page)
				time.sleep(1)
			except NoSuchElementException:
				break
		driver.close()
		return urls_list
		
class Fato_ou_fake():
	
	def __init__(self):
		self.__baseUrl = 'https://g1.globo.com/fato-ou-fake/'
		self.news_class ="feed-media-wrapper"
		self.feed_class = "feed-placeholder"
		self.news_xpath = '//div[@data-type ="materia"]'
		self.button_xpath = "//*[contains(text(), 'Veja mais')]"
		self.next_page_class = "load-more"
		self.scroll_initial = 0
		self.scroll_final = 10000
		self.scroll_add = 1000
		self.agency = 'fato_ou_fake'

	def execute_routine(self):
		urls = get_last_urls(self.agency)
		url = urls[0]
		url_news = self.crawler_news(url)
		write_routine(url_news,self.agency)
		return url_news
	def convert_date(self,text_date):
		pass
	def crawler_news(self,last_url):
		urls_list = []
		driver = webdriver.Firefox()
		driver.get(self.__baseUrl)
		#scroll page
		for i in range(0,4):
			driver.execute_script("window.scrollTo("+str(self.scroll_initial)+", "+str(self.scroll_final) +")")
			time.sleep(1)
			self.scroll_initial = self.scroll_final
			self.scroll_final += self.scroll_add
		#crawl
		while True:
			time.sleep(2)
			#news = driver.find_elements_by_class_name(self.news_class)
			feed =  WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, self.feed_class)))
			news = driver.find_elements_by_xpath(self.news_xpath)
			for n in news:
				url = n.find_element_by_tag_name('a').get_attribute("href")
				if url == last_url:
					driver.close()
					return urls_list
				urls_list.append(url)
				print(url)			
			try:
				#button = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, self.button_xpath)))
				#button = driver.find_element_by_xpath(self.button_xpath)
				#driver.execute_script("arguments[0].scrollIntoView();", button)
				#driver.execute_script("arguments[0].click();", button)
				button = driver.find_element_by_class_name(self.next_page_class)
				next_page = button.find_element_by_tag_name('a').get_attribute("href")
				driver.get(next_page)
				time.sleep(5)
			except NoSuchElementException:
				break


		driver.close()
		return urls_list
		
class Estadao_verifica():
	def __init__(self):
		self.__baseUrl = 'https://politica.estadao.com.br/blogs/estadao-verifica/'
		self.feed_class = (By.CLASS_NAME,"paged-content")
		self.news_class = (By.CSS_SELECTOR, ".col-md-6:nth-child(2)")#(By.CLASS_NAME,"col-md-6")
		self.button_class = (By.CSS_SELECTOR, ".more-list-news") 
		self.thumb_img_locator = (By.TAG_NAME, 'img')
		self.n_max_clicks = 180
		self.agency = 'estadao_verifica'
	def crawler_news(self,last_url):
		urls_list = []
		driver = webdriver.Firefox()
		driver.get(self.__baseUrl)
		n_clicks = 0
		while n_clicks < self.n_max_clicks:
			try:
				button = WebDriverWait(driver, 30).until(EC.presence_of_element_located(self.button_class))
				#button = driver.find_element_by_xpath(self.button_xpath)
				driver.execute_script("arguments[0].scrollIntoView();", button)
				driver.execute_script("arguments[0].click();", button)
				n_clicks+=1
				time.sleep(2)
			except TimeoutException:
				break
		feed = WebDriverWait(driver, 30).until(EC.presence_of_element_located(self.feed_class))
		news = driver.find_elements(*self.news_class)
		for n in news:
			wrapper_obj = n.find_element(By.TAG_NAME, 'a')
			url = wrapper_obj.get_attribute('href')
			img = wrapper_obj.find_element(By. TAG_NAME,'img')
			img_link = img.get_attribute('src')
			if url == last_url:
				driver.close()
				urls_list = urls_list[2:]
				return urls_list
			if url == 'javascript:void(0);' or url == '0':
				pass
			else:	
				urls_list.append((url,img_link))
		driver.close()
		urls_list = urls_list[2:]
		return urls_list

	def execute_routine(self):
		urls = get_last_urls(self.agency)
		url = urls[0]
		url_news = self.crawler_news(url)
		write_routine(url_news,self.agency)
		return url_news


L = Lupa()
C = Comprova()
B = Boatos()
A = Aos_fatos()
F = Fato_ou_fake()
E = E_farsas()
EV = Estadao_verifica()

#d = EV.crawler_news('https://politica.estadao.com.br/blogs/estadao-verifica/foto-viral-mostra-visita-do-papa-ao-rio-nao-ato-pro-bolsonaro-de-1o-de-maio/')
collect_all(L)
collect_all(C)
collect_all(B)
collect_all(A)
collect_all(E)
#lista = EV.crawler_news(' ')

'''
file = open("Urls/urls_estadao_verifica_com_thumb.txt",'w')
file.write(str(len(lista))+'\n')
for line in lista:
	file.write(str(line) +'\n')
	print('Escreveu!')
file.close()
'''