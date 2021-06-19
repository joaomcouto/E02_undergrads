from news_crawler.base_scrapper import BaseScrapper
from selenium.webdriver.common.by import By
from datetime import datetime

class TIERRAPURAScrapper(BaseScrapper):
    def __init__(self,interface):
        if interface:
            super(TIERRAPURAScrapper, self).__init__("firefox")
        else:
            super(TIERRAPURAScrapper, self).__init__()

    scrapperSource = "TIERRAPURA"

    main_wrapper_locator = (By.ID ,'page' )

    title_locator = (By.CLASS_NAME,'col-md-12')
    title_locator_internal = (By.CLASS_NAME,'entry-title')

    text_locator = (By.XPATH,'//div[contains(@class, "entry-content")]/div[contains(@class, "entry-content")]')
    #text_locator = (By.CLASS_NAME,'//div[contains(@class, "entry-content")/p[not(a)]')
    text_locator_internal = (By.TAG_NAME,'p' )
    textUndesirables = ['Lea tamb', 'Evite la']

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
    yearNeedsMapper = False

    category_locator = 'NULL'
    category_locator_internal = "NULL"
    addUrlCategories = False
    urlCategoryLowerBounds = ['']
    urlCategoryUpperBounds = ['']
    addTagsCategories = False
    tags_categories_locator = 'NULL'
    tags_categories_locator_internal = 'NULL'
    tagsUndesirables = []

    subtitle_locator = (By.CLASS_NAME ,'subtitle')

    image_locator = (By.CLASS_NAME ,'image-full' )
    image_locator_internal = (By.TAG_NAME, "img")
    image_locator_attribute = 'src'

    author_locator =  'NULL'
    author_locator_internal = (By.XPATH, '//p[starts-with(text(),"por") or starts-with(text(),"Por")]')
    author_locator_attribute = 'NULL'

    video_locator = 'NULL'

    undesirables = []

    """
    MANUAL CATEGORIES (MUDAR DE ACORDO COM O EDITORAL SOBRE O QUAL O CRAWLING DE URLS FOR FEITO)
                Necessario pois no inicio da pandemia por exemplo no g1, noticias de covid tem apenas a categoria "ciencia-e-saude"
                Alem disso, outro exemplo, noticias de politica relacionadas a covid frequentente recebem apenas a categoria "politica"
    """
    manualCategories = []


t = TIERRAPURAScrapper(0)
#data = t.scrap_article("https://tierrapura.org/2021/05/29/buenas-noticias-la-inmunidad-natural-al-covid-19-puede-durar-toda-la-vida/")
data = t.scrap_article("https://tierrapura.org/2021/03/20/treinta-por-ciento-de-los-vacunados-morira-en-tres-meses-asegura-doctora-sherri-tempenny")
t.append_article_to_txt(data)

data2 = t.scrap_article("https://tierrapura.org/2021/04/25/neumonia-bacteriana-un-peligro-latente-por-el-uso-prolongado-de-mascarillas")
t.append_article_to_txt(data2)

t.driver.quit()
