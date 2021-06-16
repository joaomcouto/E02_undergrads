from news_crawler.base_scrapper import BaseScrapper
from selenium.webdriver.common.by import By
from datetime import datetime

class ESTUDOSNACIONAISScrapper(BaseScrapper):
    def __init__(self,interface):
        if interface:
            super(ESTUDOSNACIONAISScrapper, self).__init__("firefox")
        else:
            super(ESTUDOSNACIONAISScrapper, self).__init__()

    main_wrapper_locator = (By.ID ,'td-outer-wrap' )

    text_locator = (By.CLASS_NAME,'td-post-content.tagdiv-type')
    text_locator_internal = (By.TAG_NAME ,'p')
    textUndesirables = []

    scrapperSource = "ESTUDOSNACIONAIS"
    title_locator = (By.CLASS_NAME ,'td-post-title' )
    title_locator_internal = (By.CLASS_NAME ,"entry-title" )
    
    date_locator = (By.CLASS_NAME,'entry-date')
    date_locator_internal = "NULL"

    dateHasTime = True

    dateHasDateTimeAttribute = True
    dateTimeAttribute = "datetime"

    dateEndingSeparator = "NULL"
    dateTimeSeparator = "NULL"
    hourMinuteSeparator = "NULL"
    dayMonthYearSeparator = "NULL"
    monthNeedsMapper = False
    dateMonthMapper = {}

    subtitle_locator = (By.CLASS_NAME ,"td-post-sub-title")

    image_locator = (By.ID ,'td-full-screen-header-image' ) 
    image_locator_internal = (By.TAG_NAME, "img") 
    image_locator_attribute = 'src'

    author_locator =  (By.CLASS_NAME ,'td-post-author-name')
    author_locator_internal = (By.TAG_NAME, "a") 
    author_locator_attribute = 'NULL'

    category_locator = 'NULL'
    category_locator_internal = 'NULL'
    
    addUrlCategories = False
    urlCategoryLowerBounds = []
    urlCategoryUpperBounds = []

    addTagsCategories = False
    tags_categories_locator = 'NULL'
    tags_categories_locator_internal = 'NULL'
    tagsUndesirables = []


    video_locator = 'NULL'
    video_locator_internal = 'NULL'
    video_locator_attribute = 'NULL'
    
    undesirables = []
    

    """
    MANUAL CATEGORIES (MUDAR DE ACORDO COM O EDITORAL SOBRE O QUAL O CRAWLING DE URLS FOR FEITO)
                Necessario pois no inicio da pandemia por exemplo no g1, noticias de covid tem apenas a categoria "ciencia-e-saude"
                Alem disso, outro exemplo, noticias de politica relacionadas a covid frequentente recebem apenas a categoria "politica"
    """
    manualCategories = []


t = ESTUDOSNACIONAISScrapper(0)
data = t.scrap_article("https://www.estudosnacionais.com/30957/anvisa-registra-26-novos-obitos-por-vacinas-nas-ultimas-24-horas/")
t.append_article_to_txt(data)
t.driver.quit()