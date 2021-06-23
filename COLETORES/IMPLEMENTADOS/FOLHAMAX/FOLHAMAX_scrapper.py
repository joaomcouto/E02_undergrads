from COLETORES.base_scrapper import BaseScrapper
from selenium.webdriver.common.by import By
from datetime import datetime

class FOLHAMAXScrapper(BaseScrapper):
    def __init__(self,interface):
        if interface:
            super(FOLHAMAXScrapper, self).__init__("firefox")
        else:
            super(FOLHAMAXScrapper, self).__init__()

    scrapperSource = "FOLHAMAX"

    main_wrapper_locator = (By.ID ,'middle' )

    title_locator = (By.CLASS_NAME,'Font30.linespacing')
    title_locator_internal = "NULL"

    text_locator = (By.ID,'TextSize')
    text_locator_internal = (By.TAG_NAME,'p')
    textUndesirables = []

    date_locator = (By.ID,'DestaqueSecao' )
    date_locator_internal = (By.CLASS_NAME,'Font12')
    dateHasTime = True
    dateHasDateTimeAttribute = False
    dateTimeAttribute = "NULL"
    dateStartSeparator = ", "
    dateEndingSeparator = " |"
    dateTimeSeparator = ", "
    hourMinuteSeparator = "h:"
    dayMonthYearSeparator = " de "
    monthNeedsMapper = True
    dateMonthMapper = {
        'Janeiro': 1,
        'Fevereiro': 2,
        'Março': 3,
        'Abril': 4,
        'Maio': 5,
        'Junho': 6,
        'Julho': 7,
        'Agosto': 8,
        'Setembro': 9,
        'Outubro': 10,
        'Novembro': 11,
        'Dezembro': 12
    }
    yearNeedsMapper = False

    category_locator = (By.ID ,'DestaqueSecao')
    category_locator_internal = (By.CLASS_NAME,'Font24Bold')
    addUrlCategories = True
    urlCategoryLowerBounds = ['.com/']
    urlCategoryUpperBounds = ['/']
    addTagsCategories = False
    tags_categories_locator = 'NULL'
    tags_categories_locator_internal = 'NULL'
    tagsUndesirables = []

    subtitle_locator = (By.CLASS_NAME ,"Chapeu.line")

    image_locator = (By.CLASS_NAME ,'img-wrapper.img-left' )
    image_locator_internal = (By.TAG_NAME, "img")
    image_locator_attribute = 'src'

    author_locator =  (By.CLASS_NAME, 'Font14.azul.linespacing')
    author_locator_internal = "NULL"
    author_locator_attribute = 'NULL'

    video_locator = 'NULL'

    undesirables = []

    """
    MANUAL CATEGORIES (MUDAR DE ACORDO COM O EDITORAL SOBRE O QUAL O CRAWLING DE URLS FOR FEITO)
                Necessario pois no inicio da pandemia por exemplo no g1, noticias de covid tem apenas a categoria "ciencia-e-saude"
                Alem disso, outro exemplo, noticias de politica relacionadas a covid frequentente recebem apenas a categoria "politica"
    """
    manualCategories = []


"""
t = FOLHAMAXScrapper(0)
data = t.scrap_article("https://www.folhamax.com/economia/renner-fechara-todas-lojas-no-brasil/253346")
t.append_article_to_txt(data)
t.driver.quit()
"""
