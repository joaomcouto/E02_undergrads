from news_crawler.base_scrapper import BaseScrapper
from selenium.webdriver.common.by import By

class ATROMBETAScrapper(BaseScrapper):
    def __init__(self,interface):
        if interface:
            super(ATROMBETAScrapper, self).__init__("firefox")
        else:
            super(ATROMBETAScrapper, self).__init__()

    text_locator = (By.CLASS_NAME,'entry-content.clearfix' )
    scrapperSource = "ATROMBETA"
    title_locator = (By.CLASS_NAME ,'entry-header' )
    main_wrapper_locator = (By.ID ,'content' )
    date_locator = (By.CLASS_NAME ,'entry-date.published' )

    title_locator_internal = (By.CLASS_NAME, 'entry-title')
    subtitle_locator = "NULL"
    image_locator = (By.CLASS_NAME ,'attachment-colormag-featured-image.size-colormag-featured-image.wp-post-image' )
    author_locator =  (By.CLASS_NAME ,'url.fn.n' )
    author_locator_attribute = 'title'
    category_locator = "NULL" #PENDING
    video_locator = "NULL"
    
    undesirables = []
    
    dateHasTime = True

    dateHasDateTimeAttribute = True
    dateTimeAttribute = 'datetime'

    dateEndingSeparator = "NULL"
    dateTimeSeparator = "NULL"
    hourMinuteSeparator = "NULL"
    dayMonthYearSeparator = "NULL"
    monthNeedsMapper = "NULL"

    addUrlCategories = False
    urlCategoryLowerBounds = [".br/"]
    urlCategoryUpperBounds = ["/2020/","/2021/"]
    """
    MANUAL CATEGORIES (MUDAR DE ACORDO COM O EDITORAL SOBRE O QUAL O CRAWLING DE URLS FOR FEITO)
                Necessario pois no inicio da pandemia por exemplo no g1, noticias de covid tem apenas a categoria "ciencia-e-saude"
                Alem disso, outro exemplo, noticias de politica relacionadas a covid frequentente recebem apenas a categoria "politica"
    """
    manualCategories = []

    image_locator_internal = "NULL"
    image_locator_attribute = 'src'

    image_locator_internal = "NULL"
    image_locator_attribute = 'src'

    text_locator_internal = (By.TAG_NAME, 'p')

t = TEMPLATEScrapper(0)
data = t.scrap_article("https://atrombetanews.com.br/2020/09/25/com-slogan-tratamento-precoce-e-vida-governo-bolsonaro-planeja-dia-d-contra-covid-em-03-de-outubro-com-kit-com-hidroxicloroquina-cloroquina-azitromicina-ivermec/")
t.append_article_to_txt(data)
t.driver.quit()