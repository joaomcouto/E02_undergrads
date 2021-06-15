from news_crawler.base_scrapper import BaseScrapper
from selenium.webdriver.common.by import By
#ERRO NA DATA
class FOCODOBRASILScrapper(BaseScrapper):
    def __init__(self,interface):
        if interface:
            super(FOCODOBRASILScrapper, self).__init__("firefox")
        else:
            super(FOCODOBRASILScrapper, self).__init__()

    main_wrapper_locator = (By.CLASS_NAME, 'noticiasingle')

    text_locator = (By.CLASS_NAME, 'noticiasingle')
    text_locator_internal = (By.TAG_NAME, 'p')
    textUndesirables = []

    scrapperSource = "FOCODOBRASIL"
    title_locator = (By.CLASS_NAME,'titulonoticia')
    title_locator_internal = "NULL"
    
    date_locator = (By.CLASS_NAME,'infopost')
    #date_locator_internal = (By.XPATH, '//a[not(contains(text(),"Atualizado"))]')
    date_locator_internal = "NULL"

    dateHasTime = True

    dateHasDateTimeAttribute = False
    dateTimeAttribute = 'NULL'

    dateEndingSeparator = " | "
    dateTimeSeparator = " "
    hourMinuteSeparator = ":"
    dayMonthYearSeparator = "/"
    monthNeedsMapper = False

    subtitle_locator = 'NULL'

    image_locator = (By.CLASS_NAME, 'moldura')
    image_locator_internal = (By.TAG_NAME, "img")
    image_locator_attribute = 'src'

    #author_locator =  (By.XPATH ,'//span[@style="color: rgb(159, 159, 223);"]' )
    author_locator = 'NULL'
    author_locator_internal = (By.TAG_NAME ,'a')
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
    


f = FOCODOBRASILScrapper(1)
data = f.scrap_article('https://focodobrasil.com/bolsonaro-afirma-que-lula-nao-ficara-elegivel/')
f.append_article_to_txt(data)
f.driver.quit()