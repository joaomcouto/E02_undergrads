from news_crawler.base_scrapper import BaseScrapper
from selenium.webdriver.common.by import By

class OLHOABERTOPRScrapper(BaseScrapper):
    def __init__(self,interface):
        if interface:
            super(OLHOABERTOPRScrapper, self).__init__("firefox")
        else:
            super(OLHOABERTOPRScrapper, self).__init__()

    main_wrapper_locator = (By.CLASS_NAME,'post-outer')
    text_locator = (By.CLASS_NAME, 'post-body')
    text_locator_internal = (By.TAG_NAME,'span')
    textUndesirables = []

    scrapperSource = "OLHOABERTOPR"
    title_locator = (By.CLASS_NAME,'post-title')
    title_locator_internal = 'NULL'
    
    date_locator = (By.CLASS_NAME,'timestamp-link')
    #date_locator_internal = (By.XPATH, '//a[not(contains(text(),"Atualizado"))]')
    date_locator_internal = (By.CLASS_NAME,'published')

    dateHasTime = True

    dateHasDateTimeAttribute = True
    dateTimeAttribute = 'title'

    dateEndingSeparator = ""
    dateTimeSeparator = ""
    hourMinuteSeparator = ""
    dayMonthYearSeparator = ""
    monthNeedsMapper = False

    subtitle_locator = 'NULL'

    image_locator = (By.TAG_NAME,'img')
    image_locator_internal = 'NULL'
    image_locator_attribute = 'src'

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
    """
    MANUAL CATEGORIES (MUDAR DE ACORDO COM O EDITORAL SOBRE O QUAL O CRAWLING DE URLS FOR FEITO)
                Necessario pois no inicio da pandemia por exemplo no g1, noticias de covid tem apenas a categoria "ciencia-e-saude"
                Alem disso, outro exemplo, noticias de politica relacionadas a covid frequentente recebem apenas a categoria "politica"
    """
    manualCategories = []
    


f = OLHOABERTOPRScrapper(1)
data = f.scrap_article('https://olhoabertopr.blogspot.com/2020/03/cuba-anuncia-que-ja-fabricou-vacina.html?fbclid=IwAR342c_F4F9DfO7t4ZM66AwmIWUMMaJLwX3jbennQauPMvLEKsSv1HE-_0U')
f.append_article_to_txt(data)
f.driver.quit()