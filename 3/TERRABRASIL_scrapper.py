from news_crawler.base_scrapper import BaseScrapper
from selenium.webdriver.common.by import By
from datetime import datetime
class TERRABRASILScrapper(BaseScrapper):
    def __init__(self,interface):
        if interface:
            super(TERRABRASILScrapper, self).__init__("firefox")
        else:
            super(TERRABRASILScrapper, self).__init__()

    main_wrapper_locator = (By.CLASS_NAME ,'post-detail' )

    text_locator = (By.CLASS_NAME,'the_content')
    text_locator_internal = (By.TAG_NAME, 'p')
    textUndesirables = []

    scrapperSource = "TERRABRASIL"
    title_locator = (By.CLASS_NAME ,'the_title' )
    title_locator_internal = (By.TAG_NAME ,"h1")
    
    date_locator = (By.CLASS_NAME ,'entry-date.published' )
    date_locator_internal = "NULL"

    dateHasTime = True

    dateHasDateTimeAttribute = True
    dateTimeAttribute = 'datetime'

    dateEndingSeparator = "NULL"
    dateTimeSeparator = "NULL"
    hourMinuteSeparator = "NULL"
    dayMonthYearSeparator = "NULL"
    monthNeedsMapper = False
    dateMonthMapper = {}

    subtitle_locator = "NULL"

    image_locator = (By.CLASS_NAME ,'post_thumb' )
    image_locator_internal = (By.TAG_NAME, "img")
    image_locator_attribute = 'src'

    #author_locator =  (By.XPATH ,'//span[@style="color: rgb(159, 159, 223);"]' )
    author_locator =  (By.CLASS_NAME ,'post_author')
    author_locator_internal = (By.TAG_NAME ,'a')
    author_locator_attribute = 'innerHTML'

    category_locator = 'NULL' 
    category_locator_internal = 'NULL'
    addUrlCategories = False
    urlCategoryLowerBounds = []
    urlCategoryUpperBounds = []

    addTagsCategories = False
    tags_categories_locator = 'NULL'
    tags_categories_locator_internal = 'NULL'
    tagsUndesirables = []


    video_locator = (By.CLASS_NAME , "wp-block-video")
    video_locator_internal =(By.TAG_NAME , "video")
    video_locator_attribute = "src"
    
    undesirables = []
    

    """
    MANUAL CATEGORIES (MUDAR DE ACORDO COM O EDITORAL SOBRE O QUAL O CRAWLING DE URLS FOR FEITO)
                Necessario pois no inicio da pandemia por exemplo no g1, noticias de covid tem apenas a categoria "ciencia-e-saude"
                Alem disso, outro exemplo, noticias de politica relacionadas a covid frequentente recebem apenas a categoria "politica"
    """
    manualCategories = []

    def get_text(self):
        ret = ""
        trechos = self.currentWrapper.find_elements(*self.text_locator)  
        for trecho in trechos:
            if(self.text_locator_internal != "NULL"):
                try:
                    paragraph =trecho.find_elements(*self.text_locator_internal)
                    paragraph = [a.get_attribute('innerHTML') for a in paragraph if not any(und in a.get_attribute('innerHTML') for und in self.textUndesirables)]
                    paragraph = " ".join(paragraph)
                except:
                    continue

            if(len(paragraph) < 20): #Capaz de tratar muitos casos de coleta acidental de lixo
                continue
            ret+= paragraph
            ret+= " "
        if(len(ret) < 30):
            raise("Texto coletado pequeno demais, algo de errado aconteceu")
        return self.treat_text(ret)


t = TERRABRASILScrapper(0)
data = t.scrap_article("https://terrabrasilnoticias.com/2021/05/bomba-documentos-mostram-coronavirus-sendo-testado-como-arma-biologica-5-anos-antes-da-pandemia-por-chineses/")
t.append_article_to_txt(data)
t.driver.quit()