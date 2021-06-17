from news_crawler.base_scrapper import BaseScrapper
from selenium.webdriver.common.by import By

class REVISTAAMAZONIAScrapper(BaseScrapper):
    def __init__(self,interface):
        if interface:
            super(REVISTAAMAZONIAScrapper, self).__init__("firefox")
        else:
            super(REVISTAAMAZONIAScrapper, self).__init__()

    main_wrapper_locator = (By.CLASS_NAME,'td-ss-main-content')
    text_locator = (By.CLASS_NAME, 'td-post-content')
    text_locator_internal = (By.TAG_NAME,'p')
    textUndesirables = []

    scrapperSource = 'REVISTAAMAZONIA'
    title_locator = (By.CLASS_NAME,'td-post-title')
    title_locator_internal = (By.CLASS_NAME,'entry-title')

    date_locator = (By.CLASS_NAME,'td-post-date')
    date_locator_internal = (By.TAG_NAME,'time')

    dateHasTime = True

    dateHasDateTimeAttribute = True
    dateTimeAttribute = 'datetime'

    dateEndingSeparator = ""
    dateTimeSeparator = ""
    hourMinuteSeparator = ""
    dayMonthYearSeparator = ""
    monthNeedsMapper = False

    subtitle_locator = 'NULL'

    image_locator = (By.CLASS_NAME,'td-post-featured-image')
    image_locator_internal = (By.CLASS_NAME,'td-modal-image')
    image_locator_attribute = 'href'

    #author_locator =  (By.XPATH ,'//span[@style="color: rgb(159, 159, 223);"]' )
    author_locator = 'NULL'
    author_locator_internal = 'NULL'
    author_locator_attribute = 'NULL'

    category_locator = 'NULL' #TEMPORARIO PQ TEM TAGS TEM QUE IMPLEMENTAR ISSO
    category_locator_internal = 'NULL'


    video_locator = "NULL"
    
    undesirables = []
    
    addUrlCategories = False
    urlCategoryLowerBounds = []
    urlCategoryUpperBounds = []

    yearNeedsMapper = False
    addTagsCategories = False
    tags_categories_locator = 'NULL'
    tags_categories_locator_internal = 'NULL'
    tagsUndesirables = []
    dateStartSeparator = "NULL"    
    """
    MANUAL CATEGORIES (MUDAR DE ACORDO COM O EDITORAL SOBRE O QUAL O CRAWLING DE URLS FOR FEITO)
                Necessario pois no inicio da pandemia por exemplo no g1, noticias de covid tem apenas a categoria "ciencia-e-saude"
                Alem disso, outro exemplo, noticias de politica relacionadas a covid frequentente recebem apenas a categoria "politica"
    """
    manualCategories = []
    


f = REVISTAAMAZONIAScrapper(1)
data = f.scrap_article('https://revistaamazonia.com.br/alemanha-envia-cobranca-de-130-bilhoes-de-libras-a-china-por-danos-causados-pelo-coronavirus/?fbclid=IwAR1wmPKZg7pn7Gx1lckrwLC56cgQmatCeq2dgLpTDwVrDkVpPGY56HcJqUM')
f.append_article_to_txt(data)
f.driver.quit()