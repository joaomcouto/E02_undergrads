from COLETORES.base_scrapper import BaseScrapper
from selenium.webdriver.common.by import By

class G1Scrapper(BaseScrapper):
    def __init__(self,interface):
        if interface:
            super(G1Scrapper, self).__init__("firefox")
        else:
            super(G1Scrapper, self).__init__()

    scrapperSource = "G1"#OBRIGATORIO NÃO NULL

    main_wrapper_locator = (By.CLASS_NAME, 'mc-body.theme') #OBRIGATORIO NÃO NULL

    title_locator = (By.CLASS_NAME,'content-head__title') #OBRIGATORIO NÃO NULL
    title_locator_internal = "NULL" #OBRIGATORIO MAS PODE SER "NULL"/VAZIO

    text_locator = (By.CLASS_NAME,'content-text__container')  #OBRIGATORIO NÃO NULL
    text_locator_internal = "NULL"#OBRIGATORIO MAS PODE SER "NULL"/VAZIO
    textUndesirables = [] #OBRIGATORIO MAS PODE SER "NULL"/VAZIO

    date_locator = (By.XPATH, '//time[@itemprop = "datePublished"]') #OBRIGATORIO NÃO NULL
    date_locator_internal = "NULL" #OBRIGATORIO MAS PODE SER "NULL"/VAZIO

    dateHasTime = True #OBRIGATORIO NÃO NULL
    dateHasDateTimeAttribute = True #OBRIGATORIO NÃO NULL
    dateTimeAttribute = "datetime" #PODE SER APAGADO SE O BOOL OBRIGATORIO ACIMA MAIS PROXIMO FOR FALSE
    

    ####Parametros abaixo desta linha são referentes a métodos que podem retornar "NULL" no caso de de erro. Acima desta linha, erros em métodos resultam em excessões que devem ser tratadas apenas para logging.
    ### Isso significa que uma coleta é considerada sucesso mesmo que os campos categories, subtitles, image_url, video_url sejam "NULL" mesmo que por motivo de excessão.

    category_locator = (By.CLASS_NAME,'header-editoria--link.ellip-line')#OBRIGATORIO MAS PODE SER "NULL"/VAZIO
    category_locator_internal = 'NULL' #PODE SER APAGADO SE O OBRIGATORIO ACIMA MAIS PROXIMO FOR "NULL"
    addUrlCategories = True #OBRIGATORIO NÃO NULL
    urlCategoryLowerBounds = [".com/"] #PODE SER APAGADO SE O BOOL OBRIGATORIO ACIMA MAIS PROXIMO FOR FALSE
    urlCategoryUpperBounds = ["/noticia"] #PODE SER APAGADO SE O BOOL OBRIGATORIO ACIMA MAIS PROXIMO FOR FALSE
    addTagsCategories = False #OBRIGATORIO NÃO NULL
    tagsUndesirables = [] #OBRIGATORIO MAS PODE SER "NULL"/VAZIO

    subtitle_locator = (By.CLASS_NAME,'content-head__subtitle') #OBRIGATORIO MAS PODE SER "NULL"/VAZIO

    image_locator = (By.TAG_NAME,'amp-img')#OBRIGATORIO MAS PODE SER "NULL"/VAZIO
    image_locator_internal = "NULL" #PODE SER APAGADO SE O OBRIGATORIO ACIMA MAIS PROXIMO FOR "NULL"
    image_locator_attribute = 'src'#PODE SER APAGADO SE O OBRIGATORIO ACIMA MAIS PROXIMO FOR "NULL"

    author_locator =  (By.CLASS_NAME , 'content-publication-data__from') #OBRIGATORIO MAS PODE SER "NULL"/VAZIO
    author_locator_internal = "NULL" #PODE SER APAGADO SE O OBRIGATORIO ACIMA MAIS PROXIMO FOR "NULL"
    author_locator_attribute = 'title' #OBRIGATORIO MAS PODE SER "NULL"

    video_locator = (By.CLASS_NAME, "content-video__placeholder") #OBRIGATORIO MAS PODE SER "NULL"/VAZIO
    video_locator_internal = 'NULL' #PODE SER APAGADO SE O OBRIGATORIO ACIMA MAIS PROXIMO FOR "NULL"
    video_locator_attribute = 'NULL'#PODE SER APAGADO SE O OBRIGATORIO ACIMA MAIS PROXIMO FOR "NULL"

    undesirables = ['/blog','/post','/especiais','/quiz'] #OBRIGATORIO MAS PODE SER "NULL"/VAZIO

    manualCategories = ['coronavirus']

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
        
    def get_category(self, articleUrl):
        categories = []
        if(self.category_locator != "NULL"):
            if(self.category_locator_internal == "NULL"):
                categoryElement =self.driver.find_element(*self.category_locator)
            else:
                categoryElement =self.driver.find_element(*self.category_locator).find_element(*self.category_locator_internal)
            try:
                categories.append(self.strip_accents( categoryElement.text.lower() ))
            except Exception as e:
                print(e)
                print("Problema temporario na captura de categoria NO ARTIGO, resolucao pendente")
                pass

        if(self.addUrlCategories):
            for lower in self.urlCategoryLowerBounds:
                if(lower in articleUrl):
                    urlCategories = articleUrl.split(lower)[1]
                    break
            for upper  in self.urlCategoryUpperBounds:
                if(upper in articleUrl):
                    urlCategories = urlCategories.split(upper)[0]
                    break
            urlCategories = urlCategories.split('/')
            categories.extend(urlCategories)

        categories.extend(self.manualCategories)
        return list(set(categories))
"""
G1 = G1Scrapper(0)
data = G1.scrap_article("https://g1.globo.com/bemestar/coronavirus/noticia/2021/04/25/covid-19-ja-matou-mais-brasileiros-em-4-meses-de-2021-do-que-em-todo-ano-de-2020.ghtml")
G1.append_article_to_txt(data)
G1.driver.quit()
"""

#Imagem no topo
#G1.scrap_article("https://g1.globo.com/ciencia-e-saude/noticia/2020/02/03/chineses-que-sairam-de-cidade-em-quarentena-por-coronavirus-pedem-a-quem-ficou-para-cuidar-de-animais-de-estimacao.ghtml")

#Sem nada
#data = G1.scrap_article("https://g1.globo.com/bemestar/vacina/noticia/2021/04/25/brasil-aplicou-ao-menos-uma-dose-de-vacina-contra-covid-em-mais-de-29-milhoes-de-pessoas-aponta-consorcio-de-veiculos-de-imprensa.ghtml")
#G1.append_article_to_txt(data)
#G1.scrap_article("")

#data = G1.scrap_article("https://g1.globo.com/bemestar/coronavirus/noticia/2021/05/21/numero-de-mortes-na-pandemia-pode-ser-ate-tres-vezes-maior-do-que-o-registrado-aponta-relatorio-da-oms.ghtml")
#G1.append_article_to_txt(data)
#G1.driver.close()
