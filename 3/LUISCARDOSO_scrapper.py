from news_crawler.base_scrapper import BaseScrapper
from selenium.webdriver.common.by import By
from datetime import datetime

class LUISCARDOSOScrapper(BaseScrapper):
    def __init__(self,interface):
        if interface:
            super(LUISCARDOSOScrapper, self).__init__("firefox")
        else:
            super(LUISCARDOSOScrapper, self).__init__()

    main_wrapper_locator = (By.TAG_NAME,'article' )

    text_locator = (By.CLASS_NAME,'post-content.sa_incontent')  
    text_locator_internal = (By.TAG_NAME,'p' )
    textUndesirables = ['Acompanhe o Blog']

    scrapperSource = "LUISCARDOSO"
    
    title_locator = (By.CLASS_NAME,'post-title')
    title_locator_internal = "NULL"
    
    date_locator = (By.CLASS_NAME,'post-date' )
    date_locator_internal = (By.TAG_NAME,'time' )

    dateHasTime = True

    dateHasDateTimeAttribute = False #Ter tem mas so tem a hora, nao serve pra nada
    dateTimeAttribute = "NULL"

    dateStartSeparator = "NULL"
    dateEndingSeparator = "NULL"
    
    dateTimeSeparator = " às "
    hourMinuteSeparator = ":"
    dayMonthYearSeparator = " de "
    monthNeedsMapper = True
    dateMonthMapper = {
        'Jan': 1,
        'Fev': 2,
        'Mar': 3,
        'Abr': 4,
        'Mai': 5,
        'Jun': 6,
        'Jul': 7,
        'Ago': 8,
        'Set': 9,
        'Out': 10,
        'Nov': 11,
        'Dez': 12
    }

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

    image_locator = 'NULL'
    image_locator_internal = 'NULL'
    image_locator_attribute = 'NULL'

    author_locator =  'NULL'
    author_locator_internal = 'NULL'
    author_locator_attribute = 'NULL'

    category_locator = (By.XPATH , '//span[i/@class = "fas fa-thumbtack"]')
    
    category_locator_internal = (By.TAG_NAME, 'a')
    
    addUrlCategories = True
    urlCategoryLowerBounds = ['.br/']
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


t = LUISCARDOSOScrapper(0)
data = t.scrap_article("https://luiscardoso.com.br/saude/2020/02/alerta-hospital-sao-domingos-registra-caso-de-crianca-com-coronavirus-em-sao-luis/?fbclid=IwAR3ZsGnHzAs_XsU3VL8sfdCF4VkYmQYsnHKSqIGbJEuNoictWj_7_f6uCpY")
t.append_article_to_txt(data)
t.driver.quit()