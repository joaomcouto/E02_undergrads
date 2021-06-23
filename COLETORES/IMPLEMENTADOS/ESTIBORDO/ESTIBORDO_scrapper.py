from COLETORES.base_scrapper import BaseScrapper
from selenium.webdriver.common.by import By
from datetime import datetime


#O get do selenium está rodando infinitamente, acredito que o site de alguma forma está bloqueando seu acesso
class ESTIBORDOScrapper(BaseScrapper):
    def __init__(self,interface):
        if interface:
            super(ESTIBORDOScrapper, self).__init__("firefox")
        else:
            super(ESTIBORDOScrapper, self).__init__()

    main_wrapper_locator = (By.CLASS_NAME ,'padded-section.grid-x.grid-padding-x.align-justify' )

    text_locator = (By.XPATH,'//section[contains(@class, "cell") and contains(@class,"medium-auto") and contains(@class, "post-content")]/p[not(strong)]')
    text_locator_internal = "NULL"
    textUndesirables = []

    scrapperSource = "ESTIBORDO"
    title_locator = (By.CLASS_NAME,'site-title.text-gray2')
    title_locator_internal = "NULL"

    date_locator = (By.CLASS_NAME,'time-badge' )
    date_locator_internal = "NULL"

    dateHasTime = False

    dateHasDateTimeAttribute = False
    dateTimeAttribute = "NULL"

    dateStartSeparator = "NULL"
    dateEndingSeparator = "NULL"

    dateTimeSeparator = "NULL"
    hourMinuteSeparator = "NULL"
    dayMonthYearSeparator = "."
    monthNeedsMapper = False
    dateMonthMapper = {}

    yearNeedsMapper = True
    dateYearMapper = {
                      '25' : 2025,
                      '24' : 2024,
                      '23' : 2023,
                      '22' : 2022,
                      '21' : 2021,
                      '20' : 2020,
                      '19' : 2019,
                      '18' : 2018,
                      '17' : 2017,
                      '16' : 2016,
                      '15' : 2015,
                      '14' : 2014,
                      '13' : 2013,
                      '12' : 2012,
                      '11' : 2011,
                      '10' : 2010,
                      '09' : 2009,
                      '08' : 2008,
                      '07' : 2007,
                      '06' : 2006,
                      '05' : 2005,
                      '04' : 2004,
                      '03' : 2003,
                      '02' : 2002,
                      '01' : 2001,
                      '00' : 2000,
    }

    subtitle_locator = "NULL"

    image_locator = (By.CLASS_NAME ,'post-image' )
    image_locator_internal = (By.TAG_NAME, "img")
    image_locator_attribute = 'src'

    author_locator =  (By.CLASS_NAME,'cell.medium-auto.post-content')

    author_locator_internal = (By.XPATH, '//p[starts-with(text(),"por") or starts-with(text(),"Por")]')
    author_locator_attribute = 'NULL'

    category_locator = (By.CLASS_NAME ,'article-badge')
    category_locator_internal = "NULL"

    addUrlCategories = False
    urlCategoryLowerBounds = ['.com/']
    urlCategoryUpperBounds = ['/']

    addTagsCategories = False
    tags_categories_locator = 'NULL'
    tags_categories_locator_internal = 'NULL'
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

    def get_text(self):
        ret = super(ESTIBORDOScrapper, self).get_text()
        ret = ret.replace(super(ESTIBORDOScrapper, self).get_author(), "")
        return ret


"""
t = ESTIBORDOScrapper(0)
data = t.scrap_article("https://www.estibordo.org/post/136667")
t.append_article_to_txt(data)
t.driver.quit()
"""
