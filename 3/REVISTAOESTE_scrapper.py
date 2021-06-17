from news_crawler.base_scrapper import BaseScrapper
from selenium.webdriver.common.by import By

class REVISTAOESTEScrapper(BaseScrapper):
    def __init__(self,interface):
        if interface:
            super(REVISTAOESTEScrapper, self).__init__("firefox")
        else:
            super(REVISTAOESTEScrapper, self).__init__()

    scrapperSource = "REVISTAOESTE"

    main_wrapper_locator = (By.CLASS_NAME ,'opened' )

    title_locator = (By.CLASS_NAME ,'entry-title' )
    title_locator_internal = "NULL"

    text_locator = (By.CLASS_NAME,'entry-content')
    text_locator_internal = (By.TAG_NAME, 'p')
    textUndesirables = ['Leia também', 'Seja nosso assinante!']

    date_locator = (By.CLASS_NAME ,'entry-date.published' )
    date_locator_internal = "NULL"
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
    urlCategoryLowerBounds = [".com/"]
    urlCategoryUpperBounds = ["/"]
    addTagsCategories = True
    tags_categories_locator = (By.CLASS_NAME ,'tags')
    tags_categories_locator_internal = (By.TAG_NAME ,'a')
    tagsUndesirables = []

    subtitle_locator = (By.CLASS_NAME ,"entry-excerpt")

    image_locator = (By.CLASS_NAME ,'entry-thumbnail' )
    image_locator_internal = (By.TAG_NAME, "img")
    image_locator_attribute = 'src'

    author_locator =  (By.CLASS_NAME ,'url.fn.n')
    author_locator_internal = "NULL"
    author_locator_attribute = 'NULL'

    video_locator = "NULL"

    undesirables = []


    """
    MANUAL CATEGORIES (MUDAR DE ACORDO COM O EDITORAL SOBRE O QUAL O CRAWLING DE URLS FOR FEITO)
                Necessario pois no inicio da pandemia por exemplo no g1, noticias de covid tem apenas a categoria "ciencia-e-saude"
                Alem disso, outro exemplo, noticias de politica relacionadas a covid frequentente recebem apenas a categoria "politica"
    """
    manualCategories = []



r = REVISTAOESTEScrapper(0)
#data = r.scrap_article("https://revistaoeste.com/brasil/novo-lote-de-insumos-sera-enviado-a-fiocruz-no-dia-21-diz-secretario/")
data = r.scrap_article("https://revistaoeste.com/mundo/ivermectina-reduziu-internacoes-por-covid-na-cidade-do-mexico/")
r.append_article_to_txt(data)
r.driver.quit()
