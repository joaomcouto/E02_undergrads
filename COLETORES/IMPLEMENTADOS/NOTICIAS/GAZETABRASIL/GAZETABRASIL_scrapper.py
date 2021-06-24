from COLETORES.base_scrapper import BaseScrapper
from selenium.webdriver.common.by import By

class GAZETABRASILScrapper(BaseScrapper):
    def __init__(self,interface):
        if interface:
            super(GAZETABRASILScrapper, self).__init__("firefox")
        else:
            super(GAZETABRASILScrapper, self).__init__()

    scrapperSource = "GAZETABRASIL"

    main_wrapper_locator = (By.CLASS_NAME ,'vc_column.tdi_90.wpb_column.vc_column_container.tdc-column.td-pb-span8' )

    title_locator = (By.CLASS_NAME ,'tdb-title-text' )
    title_locator_internal = "NULL"

    text_locator = (By.CLASS_NAME,'td_block_wrap.tdb_single_content.tdi_107.td-pb-border-top.td_block_template_1.td-post-content.tagdiv-type')
    text_locator_internal = (By.TAG_NAME, 'p')
    textUndesirables = []

    date_locator = (By.CLASS_NAME ,'td_block_wrap.tdb_single_date.tdi_98.td-pb-border-top.td_block_template_1.tdb-post-meta' )
    date_locator_internal = (By.CLASS_NAME ,"entry-date.updated.td-module-date")
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

    category_locator = 'NULL'
    category_locator_internal = 'NULL'
    addUrlCategories = True
    urlCategoryLowerBounds = [".br/"]
    urlCategoryUpperBounds = ["/2021/","/2020/"]
    addTagsCategories = False
    tagsUndesirables = []

    subtitle_locator = "NULL"

    image_locator = (By.CLASS_NAME ,'td_block_wrap.tdb_single_featured_image.tdi_102.tdb-content-horiz-left.td-pb-border-top.td_block_template_1' )
    image_locator_internal = (By.TAG_NAME, "img")
    image_locator_attribute = 'src'

    author_locator =  (By.CLASS_NAME ,'tdb-author-name-wrap')
    author_locator_internal = (By.CLASS_NAME ,'tdb-author-name')
    author_locator_attribute = 'NULL'

    video_locator = "NULL"

    undesirables = []

    """
    MANUAL CATEGORIES (MUDAR DE ACORDO COM O EDITORAL SOBRE O QUAL O CRAWLING DE URLS FOR FEITO)
                Necessario pois no inicio da pandemia por exemplo no g1, noticias de covid tem apenas a categoria "ciencia-e-saude"
                Alem disso, outro exemplo, noticias de politica relacionadas a covid frequentente recebem apenas a categoria "politica"
    """
    manualCategories = []



"""
g = GAZETABRASILScrapper(0)
data = g.scrap_article("https://gazetabrasil.com.br/especiais/coronavirus/2021/05/04/europa-comeca-a-avaliar-se-aprova-ou-nao-uso-da-coronavac/")
g.append_article_to_txt(data)
"""

#Isadora - URL DERUBADA
#data2 = g.scrap_article("https://gazetabrasil.com.br/brasil/em-video-governador-do-para-diz-que-vai-colocar-presos-para-monitorar-populacao-em-quarentena/?fbclid=IwAR0wJgjwKWr4-DC1HrHT1gkPNw2kURqYqxVzDqfS24oqxk30iGy-sU1L9Z0")
#g.append_article_to_txt(data2)

#g.driver.quit()
