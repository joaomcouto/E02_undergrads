
from news_crawler.base_scrapper import BaseScrapper
from selenium.webdriver.common.by import By
from datetime import datetime

class FOLHADAPOLITICAScrapper(BaseScrapper):
    def __init__(self,interface):
        if interface:
            super(FOLHADAPOLITICAScrapper, self).__init__("firefox")
        else:
            super(FOLHADAPOLITICAScrapper, self).__init__()

    scrapperSource = "FOLHADAPOLITICA"

    main_wrapper_locator = (By.CLASS_NAME,'post-outer' )

    title_locator = (By.CLASS_NAME,'post-head')
    title_locator_internal = (By.TAG_NAME, 'h1')

    text_locator = (By.CLASS_NAME,'post-body.entry-content')
    text_locator_internal = (By.TAG_NAME,'span' )
    textUndesirables = ['LEIA TAMBÉM:']

    date_locator = (By.CLASS_NAME,'post-timestamp' )
    date_locator_internal = (By.CLASS_NAME, 'published.timeago')
    dateHasTime = True
    dateHasDateTimeAttribute = True
    dateTimeAttribute = "title"
    dateStartSeparator = "NULL"
    dateEndingSeparator = "-07:00"
    dateTimeSeparator = "T"
    hourMinuteSeparator = ":"
    dayMonthYearSeparator = "-"
    monthNeedsMapper = False
    yearNeedsMapper = False


    category_locator = (By.CLASS_NAME, 'label-head')
    category_locator_internal = (By.TAG_NAME, 'a')
    addUrlCategories = False
    urlCategoryLowerBounds = []
    urlCategoryUpperBounds = []
    addTagsCategories = False
    tags_categories_locator = 'NULL'
    tags_categories_locator_internal = 'NULL'
    tagsUndesirables = []

    subtitle_locator = "NULL"

    image_locator = (By.CLASS_NAME, 'separator')
    image_locator_internal = (By.TAG_NAME, 'img')
    image_locator_attribute = 'src'

    author_locator = 'NULL'
    author_locator_attribute = 'NULL'

    video_locator = 'NULL'

    undesirables = []

    """
    MANUAL CATEGORIES (MUDAR DE ACORDO COM O EDITORAL SOBRE O QUAL O CRAWLING DE URLS FOR FEITO)
                Necessario pois no inicio da pandemia por exemplo no g1, noticias de covid tem apenas a categoria "ciencia-e-saude"
                Alem disso, outro exemplo, noticias de politica relacionadas a covid frequentente recebem apenas a categoria "politica"
    """
    manualCategories = []


t = FOLHADAPOLITICAScrapper(0)
data = t.scrap_article("https://www.folhadapolitica.com/2020/04/banco-mundial-classifica-o-brasil-como.html?fbclid=IwAR0bVaTHiPFLZn4ojDMkBurrVs-md9Ym-D2PUE8vjWdQFLQswAc1znmd13o")
t.append_article_to_txt(data)
t.driver.quit()
