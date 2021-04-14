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
    i=0
    while i<4:
        class_block = driver.find_elements_by_class_name("lista-noticias")
        for block in class_block:
            elements = block.find_elements_by_tag_name("a")
        for el in elements:
            url_list.add(el.get_attribute("href"))
        time.sleep(1)
        try:
            
            button = driver.find_element_by_css_selector(".btn-mais")
            driver.get(button.get_attribute("href"))
            #driver.execute_script("arguments[0].click();", button)
            time.sleep(1)
        except NoSuchElementException:
            break
        i+=1
    driver.close
    return url_list

def crawler_fato_fake():
    base_url = 'https://g1.globo.com/fato-ou-fake/'
    url_list = []
    driver = webdriver.Firefox()
    driver.get(base_url)
    class_block = driver.find_elements_by_xpath("/html/body/div[2]/main/div[4]/div[2]/div/div/div/div/div/div/div")
    for block in class_block:
        elements = driver.find_elements_by_tag_name("a")
    
    for el in elements:

        url_list.append(el.get_attribute("href"))

    return url_list

def crawler_aos_fatos():
	base_url = 'https://www.aosfatos.org/noticias/'
	url_list = set()
	driver = webdriver.Firefox()
	driver.get(base_url)
	while True:
		elements = driver.find_elements_by_css_selector(".entry-card-list>a")
		for el in elements:
			print(el.get_attribute("href"))
			url_list.add(el.get_attribute("href"))
		try:
			next_page = driver.find_element_by_class_name("next-arrow")
			next_page_url = next_page.get_attribute("href")
			driver.get(next_page_url)
		except:
			break

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
			print(url)
			url_list.add(url)
	return url_list


lista = crawler_comprova()
print(len(lista))
lista
