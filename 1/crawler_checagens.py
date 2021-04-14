import newspaper
from selenium import webdriver
import time
from selenium.webdriver.support.ui import WebDriverWait       
from selenium.webdriver.common.by import By       
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

#sources = ['https://piaui.folha.uol.com.br/lupa','https://www.aosfatos.org/','https://www.boatos.org/','https://projetocomprova.com.br/','https://g1.globo.com/fato-ou-fake/','https://www.e-farsas.com/']

def crawler_lupa():
    base_url = 'https://piaui.folha.uol.com.br/lupa'
    url_list = []

    driver = webdriver.Firefox()
    #driver = webdriver.Firefox(executable_path="./geckodriver")
    driver.get(base_url)

    wait = WebDriverWait(driver, 15)
    while True:
        class_block = driver.find_elements_by_class_name("lista-noticias")
        for block in class_block:
            elements = block.find_elements_by_tag_name("a")
        for el in elements:
            url_list.append(el.get_attribute("href"))
        time.sleep(1)
        try:
            #button = driver.find_element_by_xpath("//a[@class='btn-mais btnvermais']")
            button = driver.find_element_by_css_selector(".btn-mais")
            driver.execute_script("arguments[0].click();", button)
            time.sleep(1)
        except NoSuchElementException:
            break   
    driver.close
    return set(url_list)

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
    url_list = []
    driver = webdriver.Firefox()
    driver.get(base_url)
    elements = driver.find_elements_by_class_name("entry-card infinite-item")

    for el in elements:
        url_list.append(el.get_attribute("href"))

        return url_list

lista = crawler_lupa()

print(len(lista))

print(lista)