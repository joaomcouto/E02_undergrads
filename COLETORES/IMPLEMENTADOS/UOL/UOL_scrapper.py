from COLETORES.base_scrapper import BaseScrapper
from selenium.webdriver.common.by import By

class UOLScrapper(BaseScrapper):
    def __init__(self,interface):
        if interface:
            super(UOLScrapper, self).__init__("firefox")
        else:
            super(UOLScrapper, self).__init__()


    text_locator = (By.CLASS_NAME,'text')
    scrapperSource = "UOL"
    title_locator = (By.XPATH, '//i[@ia-title=""]')
    main_wrapper_locator = (By.CLASS_NAME, 'article.article-wrapper.scroll-base.clearfix.collection-item.collection-first-item')
    date_locator = (By.CLASS_NAME, 'p-author.time')


    subtitle_locator = "NULL"
    image_locator = (By.CLASS_NAME,'pinit-wraper')
    author_locator =  (By.CLASS_NAME , 'p-author-local')
    author_locator_attribute = "NULL"
    category_locator = (By.CLASS_NAME,'title-name')
    video_locator = "NULL"
    title_locator_internal = "NULL"

    undesirables = ['/videos','/colunas','/album','/reportagens-especiais', '/amp-stories', 'band.uol','stories','faq']

    dateHasDateTimeAttribute =True
    dateTimeAttribute = 'ia-date-publish'

    dateEndingSeparator = "Atu"
    dateHasTime = True
    dateTimeSeparator = " "
    hourMinuteSeparator = "h"
    dayMonthYearSeparator = "/"
    monthNeedsMapper = False

    addUrlCategories = True
    urlCategoryLowerBounds = [".br/"]
    urlCategoryUpperBounds = ["/2020/","/2021/"]

    manualCategories = ['coronavirus']

    image_locator_internal = (By.TAG_NAME, 'img')
    image_locator_attribute = 'src'

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
