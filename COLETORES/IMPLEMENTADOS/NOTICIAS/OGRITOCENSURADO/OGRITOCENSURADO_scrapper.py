from COLETORES.base_scrapper import BaseScrapper
from selenium.webdriver.common.by import By

class OGRITOCENSURADOScrapper(BaseScrapper):
    def __init__(self,interface):
        if interface:
            super(OGRITOCENSURADOScrapper, self).__init__("firefox")
        else:
            super(OGRITOCENSURADOScrapper, self).__init__()

    main_wrapper_locator = (By.CLASS_NAME,'site-main')
    text_locator = (By.CLASS_NAME,'entry-content')
    text_locator_internal = (By.TAG_NAME,'p')
    textUndesirables = ['Canal Telegram – O Grito Censurado']

    scrapperSource = 'OGRITOCENSURADO'
    title_locator = (By.CLASS_NAME,'entry-title')
    title_locator_internal = 'NULL'

    date_locator = (By.CLASS_NAME,'posted-on')
    date_locator_internal = (By.TAG_NAME, 'time')

    dateHasTime = True

    dateHasDateTimeAttribute = True
    dateTimeAttribute = 'datetime'

    dateEndingSeparator = ""
    dateTimeSeparator = ""
    hourMinuteSeparator = ""
    dayMonthYearSeparator = ""
    monthNeedsMapper = False

    subtitle_locator = 'NULL'

    image_locator = "NULL"
    image_locator_internal = "NULL"
    image_locator_attribute = "NULL"

    #author_locator =  (By.XPATH ,'//span[@style="color: rgb(159, 159, 223);"]' )
    author_locator = (By.CLASS_NAME, 'author-description')
    author_locator_internal = (By.CLASS_NAME,'author-title')
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



"""
f = OGRITOCENSURADOScrapper(1)
data = f.scrap_article('https://ogritocensurado.wordpress.com/2021/06/11/diga-nao-as-drogas/')
f.append_article_to_txt(data)
f.driver.quit()
"""
