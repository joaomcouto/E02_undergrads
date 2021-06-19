from news_crawler.base_scrapper import BaseScrapper
from selenium.webdriver.common.by import By

class DIARIODOPODERScrapper(BaseScrapper):
    def __init__(self,interface):
        if interface:
            super(DIARIODOPODERScrapper, self).__init__("firefox")
        else:
            super(DIARIODOPODERScrapper, self).__init__()

    scrapperSource = "DIARIODOPODER"

    main_wrapper_locator = (By.CLASS_NAME ,'jeg_content.jeg_singlepage' )

    text_locator = (By.CLASS_NAME,'content-inner')
    text_locator_internal = (By.TAG_NAME, 'p')
    textUndesirables = []

    title_locator = (By.CLASS_NAME ,'entry-header' )
    title_locator_internal = (By.CLASS_NAME, 'jeg_post_title')

    date_locator = (By.CLASS_NAME ,'jeg_meta_date' )
    date_locator_internal = "NULL"
    dateHasTime = True
    dateHasDateTimeAttribute = False
    dateTimeAttribute = 'NULL'
    dateStartSeparator = "NULL"
    dateEndingSeparator = " |"
    dateTimeSeparator = " às "
    hourMinuteSeparator = ":"
    dayMonthYearSeparator = "/"
    monthNeedsMapper = False
    yearNeedsMapper = False

    category_locator = 'NULL' #TEMPORARIO PQ TEM TAGS TEM QUE IMPLEMENTAR ISSO
    category_locator_internal = 'NULL'
    addUrlCategories = True
    urlCategoryLowerBounds = [".br/"]
    urlCategoryUpperBounds = ["/"]
    addTagsCategories = False
    tagsUndesirables = []

    subtitle_locator = (By.CLASS_NAME, "jeg_post_subtitle")

    image_locator = (By.CLASS_NAME, 'thumbnail-container.animate-lazy' )
    image_locator_internal = (By.TAG_NAME, "img")
    image_locator_attribute = 'src'

    author_locator = (By.CLASS_NAME, 'jeg_meta_author')
    author_locator_internal = (By.TAG_NAME, 'a')
    author_locator_attribute = 'NULL'

    video_locator = "NULL"

    undesirables = []

    """
    MANUAL CATEGORIES (MUDAR DE ACORDO COM O EDITORAL SOBRE O QUAL O CRAWLING DE URLS FOR FEITO)
                Necessario pois no inicio da pandemia por exemplo no g1, noticias de covid tem apenas a categoria "ciencia-e-saude"
                Alem disso, outro exemplo, noticias de politica relacionadas a covid frequentente recebem apenas a categoria "politica"
    """
    manualCategories = []



d = DIARIODOPODERScrapper(0)
#data = d.scrap_article("https://diariodopoder.com.br/coronavirus/revisao-de-estudos-sobre-ivermectina-indica-eficacia-potencial-contra-covid-19")
data = d.scrap_article("https://diariodopoder.com.br/coronavirus/revisao-de-estudos-sobre-ivermectina-indica-eficacia-potencial-contra-covid-19")
d.append_article_to_txt(data)

data2 = d.scrap_article("https://diariodopoder.com.br/politica/brasil-e-o-quinto-pais-que-mais-vacina-desde-o-dia-17-inicio-da-imunizacao")
d.append_article_to_txt(data2)
d.driver.quit()
