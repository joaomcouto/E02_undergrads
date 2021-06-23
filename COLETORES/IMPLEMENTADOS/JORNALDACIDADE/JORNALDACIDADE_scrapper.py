from COLETORES.base_scrapper import BaseScrapper
from selenium.webdriver.common.by import By
from datetime import datetime

class JORNALDACIDADEScrapper(BaseScrapper):
    def __init__(self,interface):
        if interface:
            super(JORNALDACIDADEScrapper, self).__init__("firefox")
        else:
            super(JORNALDACIDADEScrapper, self).__init__()

    scrapperSource = "JORNALDACIDADE"

    main_wrapper_locator = (By.CLASS_NAME ,'content' )

    title_locator = (By.CLASS_NAME ,'post__title' )
    title_locator_internal = "NULL"

    text_locator = (By.XPATH,'//div[contains(@class, "post__description")]/*[self::p or self::blockquote]')
    text_locator_internal = "NULL"
    textUndesirables = []

    date_locator = (By.CLASS_NAME,'post__date')
    date_locator_internal = "NULL"
    dateHasTime = True
    dateHasDateTimeAttribute = False
    dateTimeAttribute = "NULL"
    dateStartSeparator = "NULL"
    dateEndingSeparator = "NULL"
    dateTimeSeparator = " às "
    hourMinuteSeparator = ":"
    dayMonthYearSeparator = "/"
    monthNeedsMapper = False
    yearNeedsMapper = False

    category_locator = (By.CLASS_NAME ,'post__category')
    category_locator_internal = 'NULL'
    addUrlCategories = False
    urlCategoryLowerBounds = []
    urlCategoryUpperBounds = []
    addTagsCategories = True
    tags_categories_locator = (By.CLASS_NAME ,'post__tags')
    tags_categories_locator_internal = (By.CLASS_NAME ,'tag')
    tagsUndesirables = []

    subtitle_locator = "NULL"

    image_locator = (By.CLASS_NAME ,'featured-image' )
    image_locator_internal = (By.TAG_NAME, "img")
    image_locator_attribute = 'srcset'

    author_locator =  (By.CLASS_NAME ,'writer__redaction')
    author_locator_internal = 'NULL'
    author_locator_attribute = 'NULL'

    video_locator = 'NULL'

    undesirables = []

    """
    MANUAL CATEGORIES (MUDAR DE ACORDO COM O EDITORAL SOBRE O QUAL O CRAWLING DE URLS FOR FEITO)
                Necessario pois no inicio da pandemia por exemplo no g1, noticias de covid tem apenas a categoria "ciencia-e-saude"
                Alem disso, outro exemplo, noticias de politica relacionadas a covid frequentente recebem apenas a categoria "politica"
    """
    manualCategories = []


"""
t = JORNALDACIDADEScrapper(0)
data = t.scrap_article("https://www.jornaldacidadeonline.com.br/noticias/19824/roberto-kalil-reforca-testemunho-sobre-a-eficacia-da-cloroquina-no-combate-ao-coronavirus")
t.append_article_to_txt(data)
t.driver.quit()
"""
