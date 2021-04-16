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
	flag = False
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
		print(url_news)
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
		print("ULTIMA-> ",url)
		print("data: ", date)

		#crawler 
		url_news = self.crawler_news(url,date)
		print(url_news)
		#return to DB

#class E_Farsas()
		

L = Lupa()
C = Comprova()


	


