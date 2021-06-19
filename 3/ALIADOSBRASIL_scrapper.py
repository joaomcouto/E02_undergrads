from news_crawler.base_scrapper import BaseScrapper
from selenium.webdriver.common.by import By

class ALIADOSBRASILScrapper(BaseScrapper):
    def __init__(self,interface):
        if interface:
            super(ALIADOSBRASILScrapper, self).__init__("firefox")
        else:
            super(ALIADOSBRASILScrapper, self).__init__()

    main_wrapper_locator = (By.CLASS_NAME,'single_page')
    text_locator = (By.CLASS_NAME,'post_content')
    text_locator_internal = (By.TAG_NAME,'p')
    textUndesirables = []

    scrapperSource = 'ALIADOSBRASIL'
    title_locator = (By.CLASS_NAME,'post_header')
    title_locator_internal = (By.TAG_NAME,'h2')

    date_locator = (By.CLASS_NAME,'post_info_date_post')
    date_locator_internal = 'NULL'

    dateHasTime = True

    dateHasDateTimeAttribute = False
    dateTimeAttribute = 'NULL'

    dateStartSeparator = "NULL"
    dateEndingSeparator = "NULL"
    dateTimeSeparator = " "
    hourMinuteSeparator = ":"
    dayMonthYearSeparator = "/"
    monthNeedsMapper = False
    yearNeedsMapper = False

    subtitle_locator = 'NULL'

    image_locator = 'NULL'
    image_locator_internal = 'NULL'
    image_locator_attribute = 'NULL'

    #author_locator =  (By.XPATH ,'//span[@style="color: rgb(159, 159, 223);"]' )
    author_locator = (By.CLASS_NAME,'post_info_author_name')
    author_locator_internal = 'NULL'
    author_locator_attribute = 'NULL'

    category_locator = (By.CLASS_NAME,'post_header') #TEMPORARIO PQ TEM TAGS TEM QUE IMPLEMENTAR ISSO
    category_locator_internal = (By.TAG_NAME,'h4')

    addTagsCategories = False
    tags_categories_locator = 'NULL' #PODE SER APAGADO SE O BOOL OBRIGATORIO ACIMA MAIS PROXIMO FOR FALSE
    tags_categories_locator_internal = "NULL" #PODE SER APAGADO SE O BOOL OBRIGATORIO ACIMA MAIS PROXIMO FOR FALSE
    tagsUndesirables = [] #OBRIGATORIO MAS PODE SER "NULL"/VAZIO

    video_locator = 'NULL' #OBRIGATORIO MAS PODE SER "NULL"/VAZIO
    video_locator_internal = 'NULL' #PODE SER APAGADO SE O OBRIGATORIO ACIMA MAIS PROXIMO FOR "NULL"
    video_locator_attribute = 'NULL'#PODE SER APAGADO SE O OBRIGATORIO ACIMA MAIS PROXIMO FOR "NULL"
    
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
    


f = ALIADOSBRASILScrapper(0)
data = f.scrap_article('https://www.aliadosbrasiloficial.com.br/noticia/prefeitura-de-sorocaba-sp-anuncia-eficacia-de-99-do-tratamento-precoce-contra-covid')
f.append_article_to_txt(data)
f.driver.quit()