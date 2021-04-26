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
	filename = "Dump/dump_" +agency+ ".txt"
	db = open(filename,"r")
	for line in db:
		urls.append(line)
	db.close()
	return urls

def list_to_txt(urls,agency):
	d_filename = "Dump/dump_"+agency+".txt"
	r_filename = "Routines/routine"+agency+".txt"
	#r_filename = "Urls/urls_"+agency+".txt"
	r_file = open(r_filename,"a")
	d_file = open(d_filename,"w")
	#r_file.write(str(len(urls))+'\n') 
	r_file.write(str(date.today())+'\n')
	
	last_url = urls[0]
	d_file.write(last_url.strip()+'\n')
	d_file.close()
	for u in urls:
		r_file.write(u+'\n')
	r_file.close()



class Lupa():
	def __init__(self):
		self.__baseUrl  = 'https://piaui.folha.uol.com.br/lupa'
		self.date_locator = (By.CLASS_NAME,"bloco-meta")
		self.button_locator = (By.CSS_SELECTOR,".btn-mais")
		self.news_locator = (By.CSS_SELECTOR,".internaPGN > div")
		
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
				#raw_date = n.find_element(*self.date_locator).text
				#date = self.convert_date(raw_date)
				#if date >= last_date:
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
		urls = get_last_urls('lupa')
		url = urls[0]
		url_news = self.crawler_news(url)
		list_to_txt(url_news,'lupa')
		return url_news

class Comprova(): 
	def __init__(self):
		self.__baseUrl  = 'https://projetocomprova.com.br/'
		self.date_locator = (By.CLASS_NAME,"answer__credits__date")
		self.pagination_locator = (By.CSS_SELECTOR,".pagination>a")
		self.news_locator = (By.TAG_NAME,'article')
		self.news_child_locator = (By.CLASS_NAME,"answer__title__link")

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
		#get from DB
		urls = get_last_urls('comprova')

		line = urls[0].split(" ")
		url = line[0]
		#str_date = line[1].split("/")
		#date = datetime.date(int(str_date[2]),int(str_date[1]),int(str_date[0]))
		
		#crawler 
		urls_news = self.crawler_news(url)
		list_to_txt(urls_news,'comprova')
		#return to DB
		return urls_news

class E_farsas():
	
	def __init__(self):
		self.__baseUrl = 'https://www.e-farsas.com/secoes/falso-2'
		#self.news_father_locator = (By.CLASS_NAME,'wpb_wrapper')
		self.news_locator = (By.CLASS_NAME,'entry-title')
		self.button_locator = (By.XPATH,"//a[@aria-label='next-page']")

	def execute_routine(self):
		urls = get_last_urls('e_farsas')
		line = urls[0]
		urls_routine = self.crawler_news(line.strip())
		list_to_txt(urls_routine,'e_farsas')
		return urls_routine

	def convert_date(self,text_date):
		pass

	def crawler_news(self,last_url):
		urls_list = []
		driver = webdriver.Firefox()
		driver.get(self.__baseUrl)
		while True:
			news = driver.find_elements(*self.news_locator)
			for n in news:
				url = n.find_element_by_tag_name('a').get_attribute('href')
				if url == last_url:
					driver.close()
					return urls_list
				urls_list.append(url)
			try:
				button = driver.find_element(*self.button_locator)
				next_page = button.get_attribute('href')
				driver.get(next_page)
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

	def execute_routine(self):
		urls  = get_last_urls('boatos')
		last_url = urls[0].split()
		routine_urls = self.crawler_news(last_url)
		list_to_txt(routine_urls,'boatos')
		return routine_urls

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

	def execute_routine(self):
		urls = get_last_urls('fato_ou_fake')
		#line = urls[2]
		line =" "
		routine_urls = self.crawler_news(line.strip())
		list_to_txt(routine_urls,'fato_ou_fake')
		return routine_urls
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
		self.news_class = (By.CLASS_NAME,"col-md-6")
		self.button_class = (By.CSS_SELECTOR, ".more-list-news") 
		self.n_max_clicks = 4
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
			url = n.find_element_by_tag_name('a').get_attribute('href')
			if url == last_url:
				driver.close()
				return urls_list
			if url == 'javascript:void(0);' or url == '0':
				pass
			else:	
				urls_list.append(url)
		driver.close()
		return urls_list

	def execute_routine(self):
		urls = get_last_urls('estadao_verifica')
		last_url = urls[0].strip()
		routine_urls = self.crawler_news(last_url)
		list_to_txt(routine_urls,'estadao_verifica')
		return routine_urls


L = Lupa()
C = Comprova()
B = Boatos()
A = Aos_fatos()
F = Fato_ou_fake()
E = E_farsas()
EV = Estadao_verifica()

#EV.execute_routine()
#L.execute_routine()
#C.execute_routine()
#B.execute_routine()
#F.execute_routine()
#E.execute_routine()


	


