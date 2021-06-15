from news_crawler.base_scrapper import BaseScrapper
from selenium.webdriver.common.by import By

class JORNAL21BRASILScrapper(BaseScrapper):
    def __init__(self,interface):
        if interface:
            super(JORNAL21BRASILScrapper, self).__init__("firefox")
        else:
            super(JORNAL21BRASILScrapper, self).__init__()

    main_wrapper_locator = (By.CLASS_NAME,'item-post-inner')
    text_locator = (By.CLASS_NAME, 'post-body entry-content')
    text_locator_internal = (By.TAG_NAME,'span')
    textUndesirables = ["Anúncio"]

    scrapperSource = "JORNAL21BRASIL"
    title_locator = (By.CLASS_NAME,'entry-header')
    title_locator_internal = (By.CLASS_NAME,'entry-title')
    
    date_locator = (By.CLASS_NAME,'entry-time')
    #date_locator_internal = (By.XPATH, '//a[not(contains(text(),"Atualizado"))]')
    date_locator_internal = (By.CLASS_NAME,'published')

    dateHasTime = True

    dateHasDateTimeAttribute = True
    dateTimeAttribute = 'datetime'

    dateEndingSeparator = ""
    dateTimeSeparator = ""
    hourMinuteSeparator = ""
    dayMonthYearSeparator = ""
    monthNeedsMapper = False

    subtitle_locator = 'NULL'

    image_locator = (By.CLASS_NAME,'separator')
    image_locator_internal = (By.TAG_NAME,'img')
    image_locator_attribute = 'src'

    #author_locator =  (By.XPATH ,'//span[@style="color: rgb(159, 159, 223);"]' )
    author_locator = 'NULL'
    author_locator_internal = 'NULL'
    author_locator_attribute = 'NULL'

    category_locator = 'NULL' #TEMPORARIO PQ TEM TAGS TEM QUE IMPLEMENTAR ISSO
    category_locator_internal = 'NULL'


    video_locator = "NULL"
    
    undesirables = []
    
    addUrlCategories = False
    urlCategoryLowerBounds = []
    urlCategoryUpperBounds = []
    """
    MANUAL CATEGORIES (MUDAR DE ACORDO COM O EDITORAL SOBRE O QUAL O CRAWLING DE URLS FOR FEITO)
                Necessario pois no inicio da pandemia por exemplo no g1, noticias de covid tem apenas a categoria "ciencia-e-saude"
                Alem disso, outro exemplo, noticias de politica relacionadas a covid frequentente recebem apenas a categoria "politica"
    """
    manualCategories = []
    


f = JORNAL21BRASILScrapper(1)
data = f.scrap_article('https://www.jornal21brasil.com.br/2020/03/israel-sai-na-frente-e-ja-tem-vacina.html')
f.append_article_to_txt(data)
f.driver.quit()