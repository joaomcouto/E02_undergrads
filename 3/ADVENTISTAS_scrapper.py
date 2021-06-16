from news_crawler.base_scrapper import BaseScrapper
from selenium.webdriver.common.by import By

class ADVENTISTASScrapper(BaseScrapper):
    def __init__(self, interface):
        if interface:
            super(ADVENTISTASScrapper, self).__init__("firefox")
        else:
            super(ADVENTISTASScrapper, self).__init__()

    main_wrapper_locator = (By.XPATH ,"//main[@id='main']/article" )

    text_locator = (By.CLASS_NAME,'entry-content')
    text_locator_internal = "NULL"
    textUndesirables = ['Posts relacionados:', "See author's posts"]

    scrapperSource = "ADVENTISTAS"
    title_locator = (By.CLASS_NAME ,'entry-header' )
    title_locator_internal = "NULL"

    #date_locator = (By.CLASS_NAME ,'posted-on' )
    #date_locator_internal = (By.XPATH, '//a[not(contains(text(),"Atualizado"))]')
    date_locator = (By.CLASS_NAME ,'entry-date.published' )
    date_locator_internal = "NULL"

    dateHasTime = True

    dateHasDateTimeAttribute = True
    dateTimeAttribute = 'datetime'

    dateEndingSeparator = "NULL"
    dateTimeSeparator = "NULL"
    hourMinuteSeparator = "NULL"
    dayMonthYearSeparator = "NULL"
    monthNeedsMapper = False

    subtitle_locator = "NULL"

    image_locator = (By.CLASS_NAME ,'entry-content' )
    image_locator_internal = (By.XPATH, "//p//a[@class='shutterset']/img")
    image_locator_attribute = 'src'

    #author_locator =  (By.XPATH ,'//span[@style="color: rgb(159, 159, 223);"]' )
    author_locator =  (By.CLASS_NAME ,'author vcard')
    author_locator_internal = (By.TAG_NAME ,'a')
    author_locator_attribute = 'NULL'

    category_locator = 'NULL'  #TEMPORARIO PENDENTE IMPLEMENTACAO DE TAGS
    category_locator_internal = 'NULL'
    addUrlCategories = False
    urlCategoryLowerBounds = []
    urlCategoryUpperBounds = []

    addTagsCategories = False
    tags_categories_locator = (By.CLASS_NAME ,'td-tags.td-post-small-box.clearfix')
    tags_categories_locator_internal = (By.TAG_NAME ,'li')
    tagsUndesirables = ["TAGS"]


    video_locator = "NULL"#(By.CLASS_NAME ,"wp-block-video")
    video_locator_internal = (By.TAG_NAME ,"video")
    video_locator_attribute = "src"

    undesirables = []


    """
    MANUAL CATEGORIES (MUDAR DE ACORDO COM O EDITORAL SOBRE O QUAL O CRAWLING DE URLS FOR FEITO)
                Necessario pois no inicio da pandemia por exemplo no g1, noticias de covid tem apenas a categoria "ciencia-e-saude"
                Alem disso, outro exemplo, noticias de politica relacionadas a covid frequentente recebem apenas a categoria "politica"
    """
    manualCategories = []



q = ADVENTISTASScrapper(0)
data = q.scrap_article("http://www.adventistas.com/2020/04/02/novo-coronavirus-tem-algo-errado-com-esse-virus-da-covid19/")
q.append_article_to_txt(data)
q.driver.quit()
