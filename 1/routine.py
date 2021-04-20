#from news_crawler.base_crawler import BaseCrawler

from selenium import webdriver
import datetime
import time
from selenium.webdriver.support.ui import WebDriverWait       
from selenium.webdriver.common.by import By       
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

def get_last_urls(agency):
	urls = []
	filename = "Dump/dump_" +agency+ ".txt"
	db = open(filename,"r")
	for line in db:
		urls.append(line)
	db.close()
	return urls


class Lupa():
	def __init__(self):
		self.__baseUrl  = 'https://piaui.folha.uol.com.br/lupa'
		self.date_class = "bloco-meta"
		self.button_css_selector = ".btn-mais"
		self.news_css_selector = ".internaPGN > div"
		

	def convert_date(self,text_date):
		text_date = text_date.split(" | ")
		complete_date = text_date[0].split(".")
		day = int(complete_date[0])
		month = int(complete_date[1])
		year = int(complete_date[2])
		date  = datetime.date(year,month,day)
		return date

	

	def crawler_news(self,last_url,last_date):
		driver = webdriver.Firefox()
		driver.get(self.__baseUrl)
		url_list = []
		
		
		while True:
			news = driver.find_elements_by_css_selector(self.news_css_selector)
			for n in news:
				url = n.find_element_by_tag_name('a').get_attribute("href")
				raw_date = n.find_element_by_class_name(self.date_class).text
				date = self.convert_date(raw_date)
				if date >= last_date:
					if (date == last_date ) and (url == last_url):
						driver.close()
						return url_list
					url_list.append(url)
			try:
				time.sleep(1)
				button = driver.find_element_by_css_selector(self.button_css_selector)
				driver.get(button.get_attribute("href"))
			except NoSuchElementException:
				break
		driver.close()
		return url_list


	def execute_routine(self):
		#get from DB
		urls = get_last_urls('lupa')

		line = urls[0].split(" ")
		url = line[0]
		str_date = line[1].split("/")
		date = datetime.date(int(str_date[2]),int(str_date[1]),int(str_date[0]))

		#crawler 
		url_news = self.crawler_news(url,date)
		return url_news
		#return to DB

class Comprova(): 
	def __init__(self):
		self.__baseUrl  = 'https://projetocomprova.com.br/'
		self.date_class = "answer__credits__date "
		self.pagination_css_selector = ".pagination>a"
		self.news_father_tag = "article"
		self.news_child_class = "answer__title__link"

	def convert_date(self,text_date):
		#exemple : 2021-03-05
		complete_date = text_date.split("-")
		date = datetime.date(int(complete_date[0]),int(complete_date[1]),int(complete_date[2]))
		return date
	def crawler_news(self,last_url,last_date):
		page_list = []
		url_list = []
		driver = webdriver.Firefox()
		driver.get(self.__baseUrl)
		pages = driver.find_elements_by_css_selector(self.pagination_css_selector)
		for p in pages:
			page_list.append(p.get_attribute("href"))
		for page_link in page_list:
			driver.get(page_link)
			news = driver.find_elements_by_tag_name(self.news_father_tag)
			for n in news:
				url = n.find_element_by_class_name(self.news_child_class).get_attribute("href")
				raw_date = n.find_element_by_class_name(self.date_class).text
				date = self.convert_date(raw_date)
				if (date >= last_date) and (url == last_url):
					driver.close()
					return url_list
				url_list.append(url)
		driver.close()
		return url_list

	def execute_routine(self):
		#get from DB
		urls = get_last_urls('comprova')

		line = urls[0].split(" ")
		url = line[0]
		str_date = line[1].split("/")
		date = datetime.date(int(str_date[2]),int(str_date[1]),int(str_date[0]))

		#crawler 
		url_news = self.crawler_news(url,date)
		#return to DB
		return url_news

class E_farsas():
	
	def __init__(self):
		self.__baseUrl = 'https://www.e-farsas.com/secoes/falso-2'
		self.news_father_class = 'wpb_wrapper'
		self.news_class = 'entry-title'
		self.button_xpath = "//a[@aria-label='next-page']"

	def execute_routine(self):
		urls = get_last_urls('e_farsas')
		line = urls[1]
		urls_routine = self.crawler_news(line.strip())
		return urls_routine

	def convert_date(self,text_date):
		pass
	def crawler_news(self,last_url):
		urls_list = []
		driver = webdriver.Firefox()
		driver.get(self.__baseUrl)
		while True:
			news = driver.find_elements_by_class_name(self.news_class)
			for n in news:
				url = n.find_element_by_tag_name('a').get_attribute('href')
				if url == last_url:
					driver.close()
					return urls_list
				urls_list.append(url)
			try:
				button = driver.find_element_by_xpath(self.button_xpath)
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
		self.pagination_css_selector = '#archives-4 > ul:nth-child(2) > li'
		self.news_class = "entry-title"
		self.date_class = 'entry-date'
		self.button_css_selector = '.previous'

	def execute_routine(self):
		urls  = get_last_urls('boatos')
		line = urls[2].split()
		last_url = line[0]

		routine_urls = self.crawler_news(last_url)
		return routine_urls

	def convert_date(self,text_date):
		pass
	def crawler_news(self,last_url):
		archive_list = []
		urls_list = []
		driver = webdriver.Firefox()
		driver.get(self.__baseUrl)

		archive = driver.find_elements_by_css_selector(self.pagination_css_selector)
		for ar in archive:
			ar_url = ar.find_element_by_tag_name("a").get_attribute("href")
			archive_list.append(ar_url)
		for page in archive_list:
			driver.get(page)
			while True:
				time.sleep(1)
				news = driver.find_elements_by_class_name(self.news_class)
				for n in news:
					url = n.find_element_by_tag_name("a").get_attribute("href")
					if url == last_url:
						driver.close()
						return urls_list
					urls_list.append(url)
				try:
					button = driver.find_element_by_css_selector(self.button_css_selector)
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
		self.news_css_selector ='.entry-card-list>a'
		self.button_class = 'next-arrow'

	def execute_routine(self):
		urls = get_last_urls('aos_fatos')
		line = urls[2]
		routine_urls = self.crawler_news(line.strip())
		return routine_urls



	def convert_date(self,text_date):
		pass
	def crawler_news(self,last_url):
		urls_list = []
		driver = webdriver.Firefox()
		driver.get(self.__baseUrl)
		while True:
			news = driver.find_elements_by_css_selector(self.news_css_selector)
			for n in news:
				url = n.get_attribute("href")
				if url == last_url:
					driver.close()
					return urls_list
				urls_list.append(url)
			try:
				button = driver.find_element_by_class_name(self.button_class)
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
		self.button_xpath = "//*[contains(text(), 'Veja mais')]"
		self.scroll_initial = 0
		self.scroll_final = 10000
		self.scroll_add = 1000

	def execute_routine(self):
		urls = get_last_urls('fato_ou_fake')
		line = urls[2]
		routine_urls = self.crawler_news(line.strip())
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
			news = driver.find_elements_by_class_name(self.news_class)
			for n in news:
				url = n.find_element_by_tag_name('a').get_attribute("href")
				if url == last_url:
					driver.close()
					return urls_list
				urls_list.append(url)
			try:
				button = driver.find_element_by_xpath(self.button_xpath)
				next_page = button.get_attribute("href")
				driver.get(next_page)
			except NoSuchElementException:
				break
		driver.close()
		return urls_list
		

L = Lupa()
C = Comprova()
B = Boatos()
A = Aos_fatos()
F = Fato_ou_fake()
E = E_farsas()


	


