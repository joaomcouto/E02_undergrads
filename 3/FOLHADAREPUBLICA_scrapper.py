from news_crawler.base_scrapper import BaseScrapper
from selenium.webdriver.common.by import By

class FOLHADAREPUBLICAScrapper(BaseScrapper):
    def __init__(self,interface):
        if interface:
            super(FOLHADAREPUBLICAScrapper, self).__init__("firefox")
        else:
            super(FOLHADAREPUBLICAScrapper, self).__init__()

    main_wrapper_locator = (By.CLASS_NAME, 'mh-content')

    text_locator = (By.CLASS_NAME, 'entry-content')
    text_locator_internal = (By.TAG_NAME, 'p')
    textUndesirables = []

    scrapperSource = "FOLHADAREPUBLICA"
    title_locator = (By.CLASS_NAME,'entry-title')
    title_locator_internal = "NULL"
    
    date_locator = (By.CLASS_NAME,'entry-meta-date')
    #date_locator_internal = (By.XPATH, '//a[not(contains(text(),"Atualizado"))]')
    date_locator_internal = (By.TAG_NAME,'a')

    dateHasTime = False

    dateHasDateTimeAttribute = False
    dateTimeAttribute = 'NULL'

    dateEndingSeparator = "."
    dateTimeSeparator = ""
    hourMinuteSeparator = ":"
    dayMonthYearSeparator = " de "
    monthNeedsMapper = True
    dateMonthMapper = {
		'janeiro': 1,
		'fevereiro': 2,
		'março': 3,
		'abril': 4,
		'maio': 5,
		'junho': 6,
		'julho': 7,
		'agosto': 8,
		'setembro': 9,
		'outubro': 10,
		'novembro': 11,
		'dezembro': 12
    }

    subtitle_locator = 'NULL'

    image_locator = (By.CLASS_NAME, 'entry-thumbnail')
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
    


f = FOLHADAREPUBLICAScrapper(0)
data = f.scrap_article('https://folhadarepublica.com/2021/06/08/senador-jorginho-mello-surpreende-renan-calheiros-e-mostra-foto-de-renan-com-lula-sem-mascara-e-confusao-toma-conta-da-cpi/')
f.append_article_to_txt(data)
f.driver.quit()