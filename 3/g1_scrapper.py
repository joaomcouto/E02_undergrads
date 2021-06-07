from news_crawler.base_scrapper import BaseScrapper
from selenium.webdriver.common.by import By

class G1Scrapper(BaseScrapper):
    def __init__(self,interface):
        if interface:
            super(G1Scrapper, self).__init__("firefox")
        else:
            super(G1Scrapper, self).__init__()

    text_locator = (By.CLASS_NAME,'content-text__container')
    scrapperSource = "G1"
    title_locator = (By.CLASS_NAME,'content-head__title')
    main_wrapper_locator = (By.CLASS_NAME, 'mc-body.theme')
    date_locator = (By.XPATH, '//time[@itemprop = "datePublished"]')

    subtitle_locator = (By.CLASS_NAME,'content-head__subtitle')
    image_locator = (By.TAG_NAME,'amp-img')
    author_locator =  (By.CLASS_NAME , 'content-publication-data__from')
    author_locator_attribute = 'title' 
    category_locator = (By.CLASS_NAME,'header-editoria--link.ellip-line')
    video_locator = (By.CLASS_NAME, "content-video__placeholder")
    title_locator_internal = "NULL"
    
    undesirables = ['/blog','/post','/especiais','/quiz']
    
    dateHasTime = True
    dateHasDateTimeAttribute = True
    dateTimeAttribute = 'datetime'

    addUrlCategories = True
    urlCategoryLowerBounds = [".com/"]
    urlCategoryUpperBounds = ["/noticia"]

    manualCategories = ['coronavirus']

    text_locator_internal = "NULL"

    def get_main_video_url(self):
        block0 = self.currentWrapper.find_element(By.XPATH , '//div[@data-block-id="0"]')
        if (block0.get_attribute('data-block-type') == 'backstage-video'):
            return "globoplay.globo.com/v/" + block0.find_element(*self.video_locator).get_attribute('data-video-id') 
        else:
            return "NULL"
        pass

    def get_main_image_url(self):
        block0 = self.currentWrapper.find_element(By.XPATH , '//div[@data-block-id="0"]')
        if (block0.get_attribute('data-block-type') == 'backstage-photo'):
            return block0.find_element(*self.image_locator).get_attribute('src') 
        else:
            return "NULL"

G1 = G1Scrapper(0)
data = G1.scrap_article("https://g1.globo.com/bemestar/coronavirus/noticia/2021/04/25/covid-19-ja-matou-mais-brasileiros-em-4-meses-de-2021-do-que-em-todo-ano-de-2020.ghtml")
G1.append_article_to_txt(data)
G1.driver.quit()

#Imagem no topo
#G1.scrap_article("https://g1.globo.com/ciencia-e-saude/noticia/2020/02/03/chineses-que-sairam-de-cidade-em-quarentena-por-coronavirus-pedem-a-quem-ficou-para-cuidar-de-animais-de-estimacao.ghtml")

#Sem nada
#data = G1.scrap_article("https://g1.globo.com/bemestar/vacina/noticia/2021/04/25/brasil-aplicou-ao-menos-uma-dose-de-vacina-contra-covid-em-mais-de-29-milhoes-de-pessoas-aponta-consorcio-de-veiculos-de-imprensa.ghtml")
#G1.append_article_to_txt(data)
#G1.scrap_article("") 

#data = G1.scrap_article("https://g1.globo.com/bemestar/coronavirus/noticia/2021/05/21/numero-de-mortes-na-pandemia-pode-ser-ate-tres-vezes-maior-do-que-o-registrado-aponta-relatorio-da-oms.ghtml")
#G1.append_article_to_txt(data)
#G1.driver.close()

