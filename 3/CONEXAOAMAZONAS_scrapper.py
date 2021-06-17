from news_crawler.base_scrapper import BaseScrapper
from selenium.webdriver.common.by import By

class CONEXAOAMAZONASScrapper(BaseScrapper):
    def __init__(self,interface):
        if interface:
            super(CONEXAOAMAZONASScrapper, self).__init__("firefox")
        else:
            super(CONEXAOAMAZONASScrapper, self).__init__()

    main_wrapper_locator = (By.ID,"navcontent")
    text_locator = (By.CLASS_NAME,'post_content')
    text_locator_internal = (By.TAG_NAME,'p')
    textUndesirables = []

    scrapperSource = "CONEXAOAMAZONAS"
    title_locator = (By.CLASS_NAME,'p_title')
    title_locator_internal = 'NULL'
    
    date_locator = (By.CLASS_NAME,'p_post_date_desktop')
    #date_locator_internal = (By.XPATH, '//a[not(contains(text(),"Atualizado"))]')
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
    

    subtitle_locator = (By.CLASS_NAME,'p_subtitle')

    image_locator = (By.CLASS_NAME,'post_cover')
    image_locator_internal = (By.TAG_NAME,'img')
    image_locator_attribute = 'src'

    #author_locator =  (By.XPATH ,'//span[@style="color: rgb(159, 159, 223);"]' )
    author_locator = (By.CLASS_NAME, 'p_author_desktop')
    author_locator_internal = (By.TAG_NAME,'img')
    author_locator_attribute = 'alt'

    category_locator = 'NULL' #TEMPORARIO PQ TEM TAGS TEM QUE IMPLEMENTAR ISSO
    category_locator_internal = 'NULL'

    addTagsCategories = False #OBRIGATORIO NÃO NULL
    tags_categories_locator = 'NULL' #PODE SER APAGADO SE O BOOL OBRIGATORIO ACIMA MAIS PROXIMO FOR FALSE
    tags_categories_locator_internal = 'NULL' #PODE SER APAGADO SE O BOOL OBRIGATORIO ACIMA MAIS PROXIMO FOR FALSE
    tagsUndesirables = [] #OBRIGATORIO MAS PODE SER "NULL"/VAZIO

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

d = CONEXAOAMAZONASScrapper(1)
data = d.scrap_article("https://www.conexaoamazonas.com/noticia/ultimo-minuto-washington-post-confirma-a-origem-do-paciente-zero-do-coronavirus")
d.append_article_to_txt(data)
d.driver.quit()