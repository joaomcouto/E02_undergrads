from COLETORES.base_scrapper import BaseScrapper
from selenium.webdriver.common.by import By
from datetime import datetime

class TRIBUNANACIONALScrapper(BaseScrapper):
    def __init__(self,interface):
        if interface:
            super(TRIBUNANACIONALScrapper, self).__init__("firefox")
        else:
            super(TRIBUNANACIONALScrapper, self).__init__()

    scrapperSource = "TRIBUNANACIONAL"

    main_wrapper_locator = (By.CLASS_NAME ,'pageNews' )

    title_locator = (By.TAG_NAME ,'h1' )
    title_locator_internal = "NULL"

    text_locator = (By.ID,'texto_release_format')
    text_locator_internal = "NULL"
    textUndesirables = []

    date_locator = (By.TAG_NAME ,'small' )
    date_locator_internal = "NULL"
    dateHasTime = True
    dateHasDateTimeAttribute = False
    dateTimeAttribute = "NULL"
    dateStartSeparator = "NULL"
    dateEndingSeparator = "min - "
    dateTimeSeparator = " às "
    hourMinuteSeparator = "h"
    dayMonthYearSeparator = "/"
    monthNeedsMapper = False
    yearNeedsMapper = False

    category_locator = (By.XPATH ,'/html/body/section/div/div/div/h2')  #Vou ter que fazer funcao custom pq ta fora do main wrapper
    category_locator_internal = 'NULL'
    addUrlCategories = False
    urlCategoryLowerBounds = []
    urlCategoryUpperBounds = []
    addTagsCategories = False
    tags_categories_locator = 'NULL'
    tags_categories_locator_internal = 'NULL'
    tagsUndesirables = []

    subtitle_locator = "NULL"

    image_locator = (By.CLASS_NAME ,'boxhtml_full' ) #Não funciona e não tenho a menor ideia do porque
    image_locator_internal = (By.TAG_NAME, "img")
    image_locator_attribute = 'src'

    author_locator =  (By.CLASS_NAME ,'fonte')
    author_locator_internal = "NULL"
    author_locator_attribute = 'NULL'

    video_locator = 'NULL'

    undesirables = []

    """
    MANUAL CATEGORIES (MUDAR DE ACORDO COM O EDITORAL SOBRE O QUAL O CRAWLING DE URLS FOR FEITO)
                Necessario pois no inicio da pandemia por exemplo no g1, noticias de covid tem apenas a categoria "ciencia-e-saude"
                Alem disso, outro exemplo, noticias de politica relacionadas a covid frequentente recebem apenas a categoria "politica"
    """
    manualCategories = []

    def get_category(self, articleUrl):
        categories = []
        if(self.category_locator != "NULL"):
            if(self.category_locator_internal == "NULL"):
                categoryElement =self.driver.find_element(*self.category_locator) #Só mudei aqui
            else:
                categoryElement =self.driver.find_element(*self.category_locator).find_element(*self.category_locator_internal) #E aqui
            try:
                categories.append(self.strip_accents( categoryElement.text.lower() ))
            except Exception as e:
                print(e)
                print("Problema temporario na captura de categoria NO ARTIGO, resolucao pendente")
                pass

        categories.extend(self.manualCategories)
        return list(set(categories))

"""
t = TRIBUNANACIONALScrapper(0)
#data = t.scrap_article("https://tribunanacional.com.br/coluna/151/passeando-pelas-redes-sociais--jair-bolsonaro-1990")
data = t.scrap_article("https://tribunanacional.com.br/noticia/1252/cientistas-pedem-desculpas-ao-mundo--por-estudo-ter-desqualificado-o-uso-da-cloroquina-no-combate-a-pandemia-e-so-pedir-desculpas-e-esta-tudo-certo")
t.driver.quit()
"""
