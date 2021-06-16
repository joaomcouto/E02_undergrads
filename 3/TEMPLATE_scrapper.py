from news_crawler.base_scrapper import BaseScrapper
from selenium.webdriver.common.by import By
from datetime import datetime

class TEMPLATEScrapper(BaseScrapper):
    def __init__(self,interface):
        if interface:
            super(TEMPLATEScrapper, self).__init__("firefox")
        else:
            super(TEMPLATEScrapper, self).__init__()

    #Por default deixei todos os locators como By.X apenas porque X provou-se o mais comum para aquele parametro
    #Mesma lógica se aplica aos booleanos e parametros attribute
    #Para facilitar o copy&paste:
        #(By.TAG_NAME,'')
        #(By.ID,'')
        #(By.XPATH,'')

    scrapperSource = "PORTALDENOTICIA" #OBRIGATORIO NÃO NULL

    main_wrapper_locator = (By.CLASS_NAME,'main') #OBRIGATORIO NÃO NULL

    title_locator = (By.CLASS_NAME,'') #OBRIGATORIO NÃO NULL
    title_locator_internal = "NULL" #OBRIGATORIO MAS PODE SER "NULL"/VAZIO

    text_locator = (By.CLASS_NAME,'')  #OBRIGATORIO NÃO NULL
    text_locator_internal = "NULL" #OBRIGATORIO MAS PODE SER "NULL"/VAZIO
    textUndesirables = [] #OBRIGATORIO MAS PODE SER "NULL"/VAZIO

    date_locator = (By.CLASS_NAME,'' ) #OBRIGATORIO NÃO NULL
    date_locator_internal = "NULL" #OBRIGATORIO MAS PODE SER "NULL"/VAZIO
    dateHasTime = True #OBRIGATORIO NÃO NULL
    dateHasDateTimeAttribute = False #OBRIGATORIO NÃO NULL
    dateTimeAttribute = "datetime" #PODE SER APAGADO SE O BOOL OBRIGATORIO ACIMA MAIS PROXIMO FOR FALSE
    dateStartSeparator = "NULL" #PODE SER APAGADO SE O BOOL OBRIGATORIO ACIMA MAIS PROXIMO FOR TRUE
    dateEndingSeparator = "NULL" #PODE SER APAGADO SE O BOOL OBRIGATORIO ACIMA MAIS PROXIMO FOR TRUE
    dateTimeSeparator = "NULL" #PODE SER APAGADO SE O BOOL OBRIGATORIO ACIMA MAIS PROXIMO FOR TRUE
    hourMinuteSeparator = "NULL" #PODE SER APAGADO SE O BOOL OBRIGATORIO ACIMA MAIS PROXIMO FOR TRUE
    dayMonthYearSeparator = "NULL" #PODE SER APAGADO SE O BOOL OBRIGATORIO ACIMA MAIS PROXIMO FOR TRUE
    monthNeedsMapper = False #PODE SER APAGADO SE O BOOL OBRIGATORIO ACIMA MAIS PROXIMO FOR TRUE
    dateMonthMapper = {} #PODE SER APAGADO SE O BOOL OBRIGATORIO ACIMA MAIS PROXIMO FOR TRUE
    yearNeedsMapper = False #PODE SER APAGADO SE O BOOL OBRIGATORIO ACIMA MAIS PROXIMO FOR TRUE
    dateYearMapper = {} #PODE SER APAGADO SE O BOOL OBRIGATORIO ACIMA MAIS PROXIMO FOR TRUE

    ####Parametros abaixo desta linha são referentes a métodos que podem retornar "NULL" no caso de de erro. Acima desta linha, erros em métodos resultam em excessões que devem ser tratadas apenas para logging.
    ### Isso significa que uma coleta é considerada sucesso mesmo que os campos categories, subtitles, image_url, video_url sejam "NULL" mesmo que por motivo de excessão.

    category_locator = (By.CLASS_NAME, '') #OBRIGATORIO MAS PODE SER "NULL"/VAZIO
    category_locator_internal = 'NULL' #PODE SER APAGADO SE O OBRIGATORIO ACIMA MAIS PROXIMO FOR "NULL"
    addUrlCategories = False #OBRIGATORIO NÃO NULL
    urlCategoryLowerBounds = [''] #PODE SER APAGADO SE O BOOL OBRIGATORIO ACIMA MAIS PROXIMO FOR FALSE
    urlCategoryUpperBounds = [''] #PODE SER APAGADO SE O BOOL OBRIGATORIO ACIMA MAIS PROXIMO FOR FALSE
    addTagsCategories = True #OBRIGATORIO NÃO NULL
    tags_categories_locator = (By.CLASS_NAME, '') #PODE SER APAGADO SE O BOOL OBRIGATORIO ACIMA MAIS PROXIMO FOR FALSE
    tags_categories_locator_internal = (By.TAG_NAME,'') #PODE SER APAGADO SE O BOOL OBRIGATORIO ACIMA MAIS PROXIMO FOR FALSE
    tagsUndesirables = [] #OBRIGATORIO MAS PODE SER "NULL"/VAZIO

    subtitle_locator = "NULL" #OBRIGATORIO MAS PODE SER "NULL"/VAZIO

    image_locator = (By.CLASS_NAME, '')#OBRIGATORIO MAS PODE SER "NULL"/VAZIO
    image_locator_internal = (By.TAG_NAME,'') #PODE SER APAGADO SE O OBRIGATORIO ACIMA MAIS PROXIMO FOR "NULL"
    image_locator_attribute = ''#PODE SER APAGADO SE O OBRIGATORIO ACIMA MAIS PROXIMO FOR "NULL"

    author_locator =  (By.CLASS_NAME, '') #OBRIGATORIO MAS PODE SER "NULL"/VAZIO
    author_locator_internal = 'NULL' #PODE SER APAGADO SE O OBRIGATORIO ACIMA MAIS PROXIMO FOR "NULL"
    author_locator_attribute = 'NULL'#PODE SER APAGADO SE O OBRIGATORIO ACIMA MAIS PROXIMO FOR "NULL"

    video_locator = (By.CLASS_NAME, '') #OBRIGATORIO MAS PODE SER "NULL"/VAZIO
    video_locator_internal = 'NULL' #PODE SER APAGADO SE O OBRIGATORIO ACIMA MAIS PROXIMO FOR "NULL"
    video_locator_attribute = 'NULL'#PODE SER APAGADO SE O OBRIGATORIO ACIMA MAIS PROXIMO FOR "NULL"
    
    undesirables = [] #OBRIGATORIO MAS PODE SER "NULL"/VAZIO
    
    """
    MANUAL CATEGORIES (MUDAR DE ACORDO COM O EDITORAL SOBRE O QUAL O CRAWLING DE URLS FOR FEITO)
                Necessario pois no inicio da pandemia por exemplo no g1, noticias de covid tem apenas a categoria "ciencia-e-saude"
                Alem disso, outro exemplo, noticias de politica relacionadas a covid frequentente recebem apenas a categoria "politica"
    """
    manualCategories = [] #OBRIGATORIO MAS PODE SER "NULL"/VAZIO


t = TEMPLATEScrapper(0)
data = t.scrap_article("http://")
t.append_article_to_txt(data)
t.driver.quit()