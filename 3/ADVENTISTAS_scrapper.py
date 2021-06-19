from news_crawler.base_scrapper import BaseScrapper
from selenium.webdriver.common.by import By
from datetime import datetime

class ADVENTISTASScrapper(BaseScrapper):
    def __init__(self,interface):
        if interface:
            super(ADVENTISTASScrapper, self).__init__("firefox")
        else:
            super(ADVENTISTASScrapper, self).__init__()

    main_wrapper_locator = (By.ID,'main' )

    text_locator = (By.CLASS_NAME,'entry-content')  
    text_locator_internal = (By.CLASS_NAME,'o9v6fnle.cxmmr5t8.oygrvhab.hcukyx3x.c1et5uql.ii04i59q' )
    textUndesirables = []

    scrapperSource = "ADVENTISTAS"
    
    title_locator = (By.CLASS_NAME,'entry-title')
    title_locator_internal = "NULL"
    
    date_locator = (By.CLASS_NAME,'entry-date.published' )
    date_locator_internal = "NULL"

    dateHasTime = True

    dateHasDateTimeAttribute = True
    dateTimeAttribute = "datetime"

    dateStartSeparator = "NULL"
    dateEndingSeparator = "NULL"
    
    dateTimeSeparator = "NULL"
    hourMinuteSeparator = "NULL"
    dayMonthYearSeparator = "NULL"
    monthNeedsMapper = False
    dateMonthMapper = {}

    yearNeedsMapper = False
    dateYearMapper = {}

    subtitle_locator = "NULL"

    image_locator = 'NULL'
    image_locator_internal = 'NULL'
    image_locator_attribute = 'NULL'

    author_locator =  (By.CLASS_NAME,'url.fn.n')
    author_locator_internal = 'NULL'
    author_locator_attribute = 'NULL'

    category_locator = 'NULL'
    category_locator_internal = 'NULL'
    
    addUrlCategories = False
    urlCategoryLowerBounds = ['']
    urlCategoryUpperBounds = ['']

    addTagsCategories = True
    tags_categories_locator = (By.CLASS_NAME, 'cat-links')
    tags_categories_locator_internal = (By.TAG_NAME,'a')
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

#Isadora E Leandro ambos tem essa
t = ADVENTISTASScrapper(0)
data = t.scrap_article("http://www.adventistas.com/2020/04/02/novo-coronavirus-tem-algo-errado-com-esse-virus-da-covid19/")
t.append_article_to_txt(data)
t.driver.quit()