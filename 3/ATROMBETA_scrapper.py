from news_crawler.base_scrapper import BaseScrapper
from selenium.webdriver.common.by import By

class TEMPLATEScrapper(BaseScrapper):
    def __init__(self,interface):
        if interface:
            super(TEMPLATEScrapper, self).__init__("firefox")
        else:
            super(TEMPLATEScrapper, self).__init__()

    ####OBRIGATORIOS
    text_locator = (By.CLASS_NAME,'entry-content.clearfix' )
    scrapperSource = "ATROMBETA"
    title_locator = (By.CLASS_NAME ,'entry-header' )
    main_wrapper_locator = (By.ID ,'content' )
    date_locator = (By.CLASS_NAME ,'entry-date.published' )

    ###PODEM SER NULL MAS PRECISAM SER DEFINIDOS
    title_locator_internal = (By.CLASS_NAME, 'entry-title')
    subtitle_locator = "NULL"
    image_locator = (By.CLASS_NAME ,'attachment-colormag-featured-image.size-colormag-featured-image.wp-post-image' )
    author_locator =  (By.CLASS_NAME ,'url.fn.n' )
    author_locator_attribute = 'title'
    category_locator = "NULL" #PENDING
    video_locator = "NULL"
    
    ###SUBSTRINGS DE URLS INDESEJADAS
    undesirables = []
    
    #PARAMETROS PARA O METODO baseScrapper.get_date()
    dateHasTime = True

    dateHasDateTimeAttribute = True
    dateTimeAttribute = 'datetime'

    dateEndingSeparator = "NULL"
    dateTimeSeparator = "NULL"
    hourMinuteSeparator = "NULL"
    dayMonthYearSeparator = "NULL"
    monthNeedsMapper = "NULL"

    #PARAMETROS PARA O METODO baseScrapper.get_category()
    addUrlCategories = False
    urlCategoryLowerBounds = [".br/"]
    urlCategoryUpperBounds = ["/2020/","/2021/"]
    """
    MANUAL CATEGORIES (MUDAR DE ACORDO COM O EDITORAL SOBRE O QUAL O CRAWLING DE URLS FOR FEITO)
                Necessario pois no inicio da pandemia por exemplo no g1, noticias de covid tem apenas a categoria "ciencia-e-saude"
                Alem disso, outro exemplo, noticias de politica relacionadas a covid frequentente recebem apenas a categoria "politica"
    """
    manualCategories = []

    #PARAMETROS ADICIONAIS PARA O METODO baseScrapper.get_main_image_url()
    image_locator_internal = "NULL"
    image_locator_attribute = 'src'

    #PARAMETROS ADICIONAIS PARA O METODO baseScrapper.get_main_video_url()
    image_locator_internal = "NULL"
    image_locator_attribute = 'src'

    #PARAMETROS get_text()
    text_locator_internal = (By.TAG_NAME, 'p')

t = TEMPLATEScrapper(0)
data = t.scrap_article("https://atrombetanews.com.br/2020/09/25/com-slogan-tratamento-precoce-e-vida-governo-bolsonaro-planeja-dia-d-contra-covid-em-03-de-outubro-com-kit-com-hidroxicloroquina-cloroquina-azitromicina-ivermec/")
t.append_article_to_txt(data)
t.driver.quit()