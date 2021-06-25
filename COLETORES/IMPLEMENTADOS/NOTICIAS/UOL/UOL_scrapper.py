from COLETORES.base_scrapper import BaseScrapper
from selenium.webdriver.common.by import By

class UOLScrapper(BaseScrapper):
    def __init__(self,interface):
        if interface:
            super(UOLScrapper, self).__init__("firefox")
        else:
            super(UOLScrapper, self).__init__()
    scrapperSource = "UOL"

    main_wrapper_locator = (By.CLASS_NAME, 'article.article-wrapper.scroll-base.clearfix.collection-item.collection-first-item')

    title_locator = (By.XPATH, '//i[@ia-title=""]')
    title_locator_internal = "NULL"

    text_locator = (By.CLASS_NAME,'text')
    text_locator_internal = "NULL" #OBRIGATORIO MAS PODE SER "NULL"/VAZIO
    textUndesirables = [] #OBRIGATORIO MAS PODE SER "NULL"/VAZIO

    date_locator = (By.CLASS_NAME, 'p-author.time')
    date_locator_internal = "NULL" #OBRIGATORIO MAS PODE SER "NULL"/VAZIO
    dateHasTime = True
    dateHasDateTimeAttribute =True
    dateTimeAttribute = 'ia-date-publish'

    ####Parametros abaixo desta linha são referentes a métodos que podem retornar "NULL" no caso de de erro. Acima desta linha, erros em métodos resultam em excessões que devem ser tratadas apenas para logging.
    ### Isso significa que uma coleta é considerada sucesso mesmo que os campos categories, subtitles, image_url, video_url sejam "NULL" mesmo que por motivo de excessão.

    category_locator = 'NULL'
    category_locator_internal = 'NULL' #PODE SER APAGADO SE O OBRIGATORIO ACIMA MAIS PROXIMO FOR "NULL"
    addUrlCategories = True
    urlCategoryLowerBounds = [".br/"]
    urlCategoryUpperBounds = ["/2020/","/2021/"]
    addTagsCategories = False #OBRIGATORIO NÃO NULL

    tagsUndesirables = [] #OBRIGATORIO MAS PODE SER "NULL"/VAZIO

    subtitle_locator = "NULL"

    image_locator = (By.CLASS_NAME,'pinit-wraper')
    image_locator_internal = (By.TAG_NAME, 'img')
    image_locator_attribute = 'src'

    author_locator =  (By.CLASS_NAME , 'p-author-local')
    author_locator_internal = 'NULL' #PODE SER APAGADO SE O OBRIGATORIO ACIMA MAIS PROXIMO FOR "NULL"
    author_locator_attribute = "NULL"

    video_locator = "NULL"
    video_locator_internal = 'NULL' #PODE SER APAGADO SE O OBRIGATORIO ACIMA MAIS PROXIMO FOR "NULL"
    video_locator_attribute = 'NULL'#PODE SER APAGADO SE O OBRIGATORIO ACIMA MAIS PROXIMO FOR "NULL"

    undesirables = ['/videos','/colunas','/album','/reportagens-especiais', '/amp-stories', 'band.uol','stories','faq']

    manualCategories = []
















    def get_text(self):
        ret = ""
        texto = self.currentWrapper.find_element(*self.text_locator)
        trechos = texto.find_elements(By.TAG_NAME, 'p')
        for trecho in trechos:
            if (len(trecho.text) > 20):  #Necessario para reduzir chances de captar lixo
                try: #Necessario para conseguir identificar quotes e botar as aspas necessarias
                    trecho.find_element(By.TAG_NAME, 'cite')
                    ret+= "'"
                    ret+= (trecho.text)
                    ret+= "'"
                    ret+= " "
                except:
                    ret+= (trecho.text)
                    ret+= " "
        return self.treat_text(ret)

"""
u = UOLScrapper(0)
# data = u.scrap_article("https://noticias.uol.com.br/politica/ultimas-noticias/2021/06/05/abraham-e-arthur-weintraub-covid-19-estados-unidos.htm")
#data = u.scrap_article("https://noticias.uol.com.br/videos/2021/05/26/doria-recua-e-adia-flexibilizacao-em-sp-em-14-dias-apos-alta-nos-casos-de-covid-19.htm")
data = u.scrap_article("https://noticias.uol.com.br/politica/ultimas-noticias/2021/06/06/nao-havia-desejo-de-mudanca-diz-hajjar-que-rejeitou-ministerio-da-saude.htm")
u.append_article_to_txt(data)
u.driver.quit()
"""


#start = time.time()
#u = UOLScrapper(0)
#u.scrap_urls_file('UOL/URL/UOL_coronavirus_882_loads.txt','historica_uol_continued')
#print("Total elapsed time:", time.time() -start)
#u.driver.quit()




#Problemas: infinite load pages gerando timeout no driver.get() e causando fechamento do ddriver:
    #Solucao:
                        #except InvalidSessionIdException as inval:
                           # logging.exception(url)
                            #super(UOLScrapper, self).__init__()
                            #break
