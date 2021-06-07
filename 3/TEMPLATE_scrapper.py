from news_crawler.base_scrapper import BaseScrapper
from selenium.webdriver.common.by import By

class TEMPLATEScrapper(BaseScrapper):
    def __init__(self,interface):
        if interface:
            super(TEMPLATEScrapper, self).__init__("firefox")
        else:
            super(TEMPLATEScrapper, self).__init__()

    ####OBRIGATORIOS
    text_locator = (By. ,'')
    scrapperSource = "TEMPLATE"
    title_locator = (By. ,'')
    main_wrapper_locator = (By. ,'')
    date_locator = (By. , )

    ###PODEM SER NULL MAS PRECISAM SER DEFINIDOS
    title_locator_internal = (By. '')
    subtitle_locator = (By. ,'')
    image_locator = (By. ,'')
    author_locator =  (By. ,'')
    author_locator_attribute = (By. ,'')
    category_locator = (By. ,'')
    video_locator = (By. ,'')
    
    ###SUBSTRINGS DE URLS INDESEJADAS
    undesirables = ['']
    
    #PARAMETROS PARA O METODO baseScrapper.get_date()
    dateHasTime = bool

    dateHasDateTimeAttribute = bool
    dateTimeAttribute = 'datetime'

    dateEndingSeparator = "NULL"
    dateTimeSeparator = "NULL"
    hourMinuteSeparator = "NULL"
    dayMonthYearSeparator = "NULL"
    monthNeedsMapper = "NULL"

    #PARAMETROS PARA O METODO baseScrapper.get_category()
    addUrlCategories = True
    urlCategoryLowerBounds = [".br/"]
    urlCategoryUpperBounds = ["/2020/","/2021/"]
    """
    MANUAL CATEGORIES (MUDAR DE ACORDO COM O EDITORAL SOBRE O QUAL O CRAWLING DE URLS FOR FEITO)
                Necessario pois no inicio da pandemia por exemplo no g1, noticias de covid tem apenas a categoria "ciencia-e-saude"
                Alem disso, outro exemplo, noticias de politica relacionadas a covid frequentente recebem apenas a categoria "politica"
    """
    manualCategories = ['','']

    #PARAMETROS ADICIONAIS PARA O METODO baseScrapper.get_main_image_url()
    image_locator_internal = (By. , )
    image_locator_attribute = ''

    #PARAMETROS ADICIONAIS PARA O METODO baseScrapper.get_main_video_url()
    video_locator_internal = "NULL"
    video_locator_attribute = 'src'

    #PARAMETROS get_text()
    text_locator_internal = "NULL"

t = TEMPLATEScrapper(0)
data = t.scrap_article("https://")
t.append_article_to_txt(data)
t.driver.quit()