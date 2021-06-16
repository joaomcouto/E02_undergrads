from news_crawler.base_scrapper import BaseScrapper
from selenium.webdriver.common.by import By

class RSAGORAScrapper(BaseScrapper):
    def __init__(self,interface):
        if interface:
            super(RSAGORAScrapper, self).__init__("firefox")
        else:
            super(RSAGORAScrapper, self).__init__()

    main_wrapper_locator = (By.TAG_NAME,'article')
    text_locator = (By.ID,'mvp-content-main')
    text_locator_internal = (By.TAG_NAME,'p')
    textUndesirables = []

    scrapperSource = "RSAGORA"
    title_locator = (By.CLASS_NAME,'mvp-post-title')
    title_locator_internal = 'NULL'

    subtitle_locator = 'NULL'
    
    date_locator = (By.CLASS_NAME,'mvp-author-info-text')
    #date_locator_internal = (By.XPATH, '//a[not(contains(text(),"Atualizado"))]')
    date_locator_internal = (By.TAG_NAME, 'time')

    dateHasTime = False

    dateHasDateTimeAttribute = True
    dateTimeAttribute = 'datetime'

    dateEndingSeparator = "NULL"
    dateTimeSeparator = " às "
    hourMinuteSeparator = ":"
    dayMonthYearSeparator = " de "
    monthNeedsMapper = False



    image_locator = (By.CLASS_NAME,'wp-caption')
    image_locator_internal = (By.TAG_NAME,'img')
    image_locator_attribute = 'src'

    #author_locator =  (By.XPATH ,'//span[@style="color: rgb(159, 159, 223);"]' )
    author_locator = (By.CLASS_NAME,'author-name')
    author_locator_internal = (By.TAG_NAME,'a')
    author_locator_attribute = 'NULL'

    category_locator = (By.CLASS_NAME, 'mvp-post-cat') #TEMPORARIO PQ TEM TAGS TEM QUE IMPLEMENTAR ISSO
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

d = RSAGORAScrapper(1)
data = d.scrap_article("https://www.rsagora.com.br/detento-solto-por-medo-do-coronavirus-e-preso-com-grande-quantidade-de-drogas-e-armas/?fbclid=IwAR2mKVYla2Zb_arsluMtY-QqZpdMhSHd3AQtXhiRaq1O_ZlOVtG0m2la4ik")
d.append_article_to_txt(data)
d.driver.quit()