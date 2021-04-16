import newspaper
from selenium import webdriver
import time
from selenium.webdriver.support.ui import WebDriverWait       
from selenium.webdriver.common.by import By       
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup

#sources = ['https://piaui.folha.uol.com.br/lupa','https://www.aosfatos.org/','https://www.boatos.org/','https://projetocomprova.com.br/','https://g1.globo.com/fato-ou-fake/','https://www.e-farsas.com/']

def crawler_lupa():
	base_url = 'https://piaui.folha.uol.com.br/lupa'
	url_list = set()

	driver = webdriver.Firefox()
	#driver = webdriver.Firefox(executable_path="./geckodriver")
	driver.get(base_url)

	wait = WebDriverWait(driver, 15)

	while True:
		class_block = driver.find_elements_by_class_name("lista-noticias")
		for block in class_block:
			elements = block.find_elements_by_tag_name("a")
		for el in elements:
			url_list.add(el.get_attribute("href"))
		try:
			time.sleep(1)
			button = driver.find_element_by_css_selector(".btn-mais")
			driver.get(button.get_attribute("href"))
			#driver.execute_script("arguments[0].click();", button)
			time.sleep(1)
		except NoSuchElementException:
			break

	driver.close()
	return url_list

def crawler_fato_fake():
	base_url = 'https://g1.globo.com/fato-ou-fake/'
	url_list = set()
	driver = webdriver.Firefox()
	driver.get(base_url)
	wait = WebDriverWait(driver, 15)
	i=0
	while True:
		feed = driver.find_element_by_id('feed-placeholder')
		elements = feed.find_elements_by_xpath('//div[@data-type ="materia"]')
		for el in elements:
			url = el.find_element_by_tag_name("a").get_attribute("href")
			url_list.add(url)
			print(url)
		try:
			time.sleep(1)
			button = driver.find_element_by_xpath("//*[contains(text(), 'Veja mais')]")
			#driver.execute_script("arguments[0].click();", button)
			driver.get(button.get_attribute("href"))

		except NoSuchElementException:
			break

	driver.close()
	return url_list
def crawler_aos_fatos():
	base_url = 'https://www.aosfatos.org/noticias/'
	url_list = set()
	driver = webdriver.Firefox()
	driver.get(base_url)

	while True:
		elements = driver.find_elements_by_css_selector(".entry-card-list>a")
		for el in elements:
			url_list.add(el.get_attribute("href"))
		try:
			next_page = driver.find_element_by_class_name("next-arrow")
			next_page_url = next_page.get_attribute("href")
			driver.get(next_page_url)
		except:
			break
	
	driver.close()	
	return url_list

def crawler_comprova():
	base_url = 'https://projetocomprova.com.br/'
	url_list = set()
	page_list = []
	driver = webdriver.Firefox()
	driver.get(base_url)
	pages = driver.find_elements_by_css_selector(".pagination>a")
	for page in pages:
		page_list.append(page.get_attribute("href"))
	for link in page_list:
		driver.get(link)
		elements = driver.find_elements_by_tag_name("article")
		for el in elements:
			url = el.find_element_by_class_name("answer__title__link").get_attribute("href")
			url_list.add(url)
			print(url)
	driver.close()
	return url_list

def crawler_e_farsas():
	base_urls = ['https://www.e-farsas.com/secoes/falso-2','https://www.e-farsas.com/secoes/verdadeiro-2']
	url_list = set()
	driver = webdriver.Firefox()
	for base_url in base_urls:
		driver.get(base_url)
		wait = WebDriverWait(driver, 15)
		f = True
		while True:
			notices = driver.find_elements_by_css_selector(".mvp-main-blog-story>li")
			for notice in notices:
				elements = driver.find_elements_by_class_name("mvp-main-blog-in")
			for el in elements:
				url = el.find_element_by_tag_name("a").get_attribute("href")
				url_list.add(url)
			try:
				if f:
					button = driver.find_element_by_css_selector(".pagination > a:nth-child(7)")
					f = False
				else:
					button = driver.find_element_by_xpath("//*[contains(text(), 'Próxima ›')]")
				#driver.execute_script("arguments[0].click();", button)
				new_page = button.get_attribute("href")
				driver.get(new_page)
				time.sleep(3)
			except NoSuchElementException:
				break

	driver.close()	
	return url_list

def crawler_boatos():
	base_url = 'https://www.boatos.org/contato'
	urls_list = set()
	urls_archive =[]
	driver = webdriver.Firefox()
	driver.get(base_url)
	archive = driver.find_elements_by_css_selector("#archives-4 > ul:nth-child(2) > li")

	for element in archive:
		ar = element.find_element_by_tag_name("a").get_attribute("href")
		urls_archive.append(ar)

	for url in urls_archive:
		driver.get(url)
		while True:
			time.sleep(1)
			titles = driver.find_elements_by_class_name("entry-title")
			for title in titles:
				link = title.find_element_by_tag_name("a").get_attribute("href")
				urls_list.add(link)
				print(link)
			try:
				button = driver.find_element_by_css_selector(".previous")
				next_page = button.find_element_by_tag_name("a").get_attribute("href")
				driver.get(next_page)
			except NoSuchElementException:
				break

	driver.close()


urls_fato_ou_fake = crawler_fato_fake()

fato_ou_fake_file = open("urls/fato_ou_fake.txt","w")
fato_ou_fake_file.write(str(len(urls_fato_ou_fake))+'\n')
for u in urls_fato_ou_fake:
	fato_ou_fake_file.write(u+'\n')
fato_ou_fake_file.close()


"""
urls_lupa = list(crawler_lupa())
urls_aos_fatos = list(crawler_aos_fatos())
urls_comprova = list(crawler_comprova())
urls_e_farsas = crawler_e_farsas()
urls_fato_ou_fake = crawler_fato_fake()
urls_boatos = crawler_boatos()

lupa_file = open("urls/urls_lupa.txt","w")
lupa_file.write(str(len(urls_lupa)) + '\n')
for u in urls_lupa:
	lupa_file.write(u + '\n')
lupa_file.close()

aos_fatos_file = open("urls/urls_aos_fatos.txt","w")
aos_fatos_file.write(str(len(urls_aos_fatos))+'\n')
for u in urls_aos_fatos:
	aos_fatos_file.write(u+'\n')
aos_fatos_file.close()

comprova_file = open("urls/urls_comprova.txt","w")
comprova_file.write(str(len(urls_comprova))+'\n')
for u in urls_comprova:
	comprova_file.write(u+'\n')
comprova_file.close()

e_farsas_file = open("urls/urls_e_farsas.txt","w")
e_farsas_file.write(str(len(urls_e_farsas))+'\n')
for u in urls_e_farsas:
	e_farsas_file.write(u+'\n')
e_farsas_file.close()

fato_ou_fake_file = open("urls/fato_ou_fake.txt","w")
fato_ou_fake_file.write(str(len(urls_fato_ou_fake))+'\n')
for u in urls_fato_ou_fake:
	fato_ou_fake_file.write(u+'\n')
fato_ou_fake_file.close()

boatos_file = open("urls/boatos.txt","w")
boatos_file.write(str(len(urls_boatos)))
for u in url_boatos:
	boatos_file.write(u+'\n')
boatos_file.close()

"""

