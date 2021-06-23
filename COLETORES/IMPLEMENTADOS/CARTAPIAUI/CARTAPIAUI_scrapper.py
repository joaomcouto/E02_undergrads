from COLETORES.base_scrapper import BaseScrapper
from selenium.webdriver.common.by import By

class CARTAPIAUIScrapper(BaseScrapper):
    def __init__(self,interface):
        if interface:
            super(CARTAPIAUIScrapper, self).__init__("firefox")
        else:
            super(CARTAPIAUIScrapper, self).__init__()

    main_wrapper_locator = (By.CLASS_NAME, 'content-inner')
    text_locator = (By.CLASS_NAME,'post-body-inner')
    text_locator_internal = (By.TAG_NAME,'p')
    textUndesirables = []

    scrapperSource = "CARTAPIAUI"
    title_locator = (By.CLASS_NAME,'post-header')
    title_locator_internal = (By.CLASS_NAME, 'post-title')

    subtitle_locator = 'NULL'

    date_locator = (By.CLASS_NAME,'post-meta-wrapper')
    #date_locator_internal = (By.XPATH, '//a[not(contains(text(),"Atualizado"))]')
    date_locator_internal = 'NULL'

    dateHasTime = True

    dateHasDateTimeAttribute = False
    dateTimeAttribute = 'NULL'

    dateStartSeparator = "NULL"
    dateEndingSeparator = "NULL"
    dateTimeSeparator = " às "
    hourMinuteSeparator = ":"
    dayMonthYearSeparator = " de "
    monthNeedsMapper = True
    yearNeedsMapper = False
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


    image_locator = 'NULL'
    image_locator_internal = (By.TAG_NAME,'img')
    image_locator_attribute = 'src'

    #author_locator =  (By.XPATH ,'//span[@style="color: rgb(159, 159, 223);"]' )
    author_locator = 'NULL'
    author_locator_attribute = 'NULL'

    category_locator = 'NULL' #TEMPORARIO PQ TEM TAGS TEM QUE IMPLEMENTAR ISSO
    category_locator_internal = 'NULL'
    addTagsCategories = False


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

"""
d = CARTAPIAUIScrapper(0)
data = d.scrap_article("https://cartapiaui.com.br/noticias/feitosa-costa/avanco-hospital-no-piaui-cura-pessoas-da-covid-19-e-esvazia-utis-com-uso-de-cloroquina-36954.html?fbclid=IwAR30hJf77Lt6YqE-MR03LalxDBcqfXRduQafmLcEbcM-qZlglcUjKhSxFR8")
d.append_article_to_txt(data)
d.driver.quit()
"""
