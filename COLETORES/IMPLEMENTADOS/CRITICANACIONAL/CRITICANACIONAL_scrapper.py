from COLETORES.base_scrapper import BaseScrapper
from selenium.webdriver.common.by import By

class CRITICANACIONALScrapper(BaseScrapper):
    def __init__(self,interface):
        if interface:
            super(CRITICANACIONALScrapper, self).__init__("firefox")
        else:
            super(CRITICANACIONALScrapper, self).__init__()

    scrapperSource = "CRITICANACIONAL"

    main_wrapper_locator = (By.CLASS_NAME ,'post.type-post' )

    title_locator = (By.CLASS_NAME ,'td-post-title' )
    title_locator_internal = (By.CLASS_NAME, 'entry-title')

    text_locator = (By.CLASS_NAME,'td-post-content.tagdiv-type')
    text_locator_internal = (By.TAG_NAME, 'p')
    textUndesirables = []

    def get_text(self):
        ret = super(CRITICANACIONALScrapper, self).get_text()
        return self.treat_text(ret.replace(super(CRITICANACIONALScrapper, self).get_author(), ""))

    date_locator = (By.CLASS_NAME ,'td-post-title' )
    date_locator_internal = (By.CLASS_NAME, 'entry-date.updated.td-module-date')
    dateHasTime = True
    dateHasDateTimeAttribute = True
    dateTimeAttribute = 'datetime'
    dateStartSeparator = "NULL"
    dateEndingSeparator = "NULL"
    dateTimeSeparator = "NULL"
    hourMinuteSeparator = "NULL"
    dayMonthYearSeparator = "NULL"
    monthNeedsMapper = False
    yearNeedsMapper = False

    category_locator = (By.CLASS_NAME, "entry-category")
    category_locator_internal = (By.TAG_NAME, "a")
    addUrlCategories = False
    addTagsCategories = False
    tagsUndesirables = []

    subtitle_locator = "NULL"

    image_locator = (By.CLASS_NAME ,'td-post-featured-image' )
    image_locator_internal = (By.TAG_NAME, "img")
    image_locator_attribute = 'src'

    author_locator =  (By.XPATH ,'//span[contains(@style,"color:")]' )
    author_locator_attribute = 'NULL'
    author_locator_internal = 'NULL'

    video_locator = "NULL"

    undesirables = []

    """
    MANUAL CATEGORIES (MUDAR DE ACORDO COM O EDITORAL SOBRE O QUAL O CRAWLING DE URLS FOR FEITO)
                Necessario pois no inicio da pandemia por exemplo no g1, noticias de covid tem apenas a categoria "ciencia-e-saude"
                Alem disso, outro exemplo, noticias de politica relacionadas a covid frequentente recebem apenas a categoria "politica"
    """
    manualCategories = []


"""
c = CRITICANACIONALScrapper(0)
data = c.scrap_article("https://criticanacional.com.br/2021/04/13/estudo-da-universidade-de-tel-aviv-pessoas-vacinadas-tem-oito-vezes-mais-chances-de-contrair-variante-do-coronavirus")
c.append_article_to_txt(data)
data2 = c.scrap_article("https://criticanacional.com.br/2021/05/24/partido-comunista-chines-oferece-ajuda-milionaria-ao-grupo-terrorista-hamas")
c.append_article_to_txt(data2)
c.driver.quit()
"""
