from news_crawler.base_scrapper import BaseScrapper
from selenium.webdriver.common.by import By

class QUESTIONESEScrapper(BaseScrapper):
    def __init__(self,interface):
        if interface:
            super(QUESTIONESEScrapper, self).__init__("firefox")
        else:
            super(QUESTIONESEScrapper, self).__init__()

    main_wrapper_locator = (By.CLASS_NAME ,'td-post-template-6' )

    text_locator = (By.CLASS_NAME,'td-post-content.tagdiv-type')
    text_locator_internal = (By.TAG_NAME, 'p')
    textUndesirables = ['VEJA TAMBÉM', 'Para mais informações acesse']

    scrapperSource = "QUESTIONESE"
    title_locator = (By.CLASS_NAME ,'td-post-title' )
    title_locator_internal = (By.CLASS_NAME , "entry-title")
    
    date_locator = (By.CLASS_NAME ,'td-post-title' )
    #date_locator_internal = (By.XPATH, '//a[not(contains(text(),"Atualizado"))]')
    date_locator_internal = (By.CLASS_NAME ,"entry-date.updated.td-module-date")

    dateHasTime = True

    dateHasDateTimeAttribute = True
    dateTimeAttribute = 'datetime'

    dateEndingSeparator = "NULL"
    dateTimeSeparator = "NULL"
    hourMinuteSeparator = "NULL"
    dayMonthYearSeparator = "NULL"
    monthNeedsMapper = False

    subtitle_locator = "NULL"

    image_locator = (By.ID ,'td-full-screen-header-image' )
    image_locator_internal = (By.TAG_NAME, "img")
    image_locator_attribute = 'src'

    #author_locator =  (By.XPATH ,'//span[@style="color: rgb(159, 159, 223);"]' )
    author_locator =  (By.CLASS_NAME ,'td-post-author-name')
    author_locator_internal = (By.TAG_NAME ,'a')
    author_locator_attribute = 'NULL'

    category_locator = 'NULL'  #TEMPORARIO PENDENTE IMPLEMENTACAO DE TAGS
    category_locator_internal = 'NULL'
    addUrlCategories = False
    urlCategoryLowerBounds = []
    urlCategoryUpperBounds = []

    addTagsCategories = True
    tags_categories_locator = (By.CLASS_NAME ,'td-tags.td-post-small-box.clearfix')
    tags_categories_locator_internal = (By.TAG_NAME ,'li')
    tagsUndesirables = ["TAGS"]


    video_locator = (By.CLASS_NAME ,"wp-block-video")
    video_locator_internal = (By.TAG_NAME ,"video")
    video_locator_attribute = "src"
    
    undesirables = []
    

    """
    MANUAL CATEGORIES (MUDAR DE ACORDO COM O EDITORAL SOBRE O QUAL O CRAWLING DE URLS FOR FEITO)
                Necessario pois no inicio da pandemia por exemplo no g1, noticias de covid tem apenas a categoria "ciencia-e-saude"
                Alem disso, outro exemplo, noticias de politica relacionadas a covid frequentente recebem apenas a categoria "politica"
    """
    manualCategories = []
    


q = QUESTIONESEScrapper(0)
data = q.scrap_article("https://terrabrasilnoticias.com/2020/07/ministro-da-educacao-milton-ribeiro-recebe-alta-do-hospital-apos-tratamento-com-hidroxicloroquina-e-antibioticos/")
q.append_article_to_txt(data)
q.driver.quit()