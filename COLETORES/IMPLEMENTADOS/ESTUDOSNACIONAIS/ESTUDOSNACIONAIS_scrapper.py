from COLETORES.base_scrapper import BaseScrapper
from selenium.webdriver.common.by import By
from datetime import datetime

class ESTUDOSNACIONAISScrapper(BaseScrapper):
    def __init__(self,interface):
        if interface:
            super(ESTUDOSNACIONAISScrapper, self).__init__("firefox")
        else:
            super(ESTUDOSNACIONAISScrapper, self).__init__()

    main_wrapper_locator = (By.CLASS_NAME ,'jeg_main.jeg_sidebar_none' )

    text_locator = (By.CLASS_NAME,'content-inner')
    text_locator_internal = (By.TAG_NAME ,'p')
    textUndesirables = []

    scrapperSource = "ESTUDOSNACIONAIS"
    title_locator = (By.CLASS_NAME ,'entry-header' )
    title_locator_internal = (By.CLASS_NAME ,"jeg_post_title" )

    date_locator = (By.CLASS_NAME,'entry-header')
    date_locator_internal = (By.CLASS_NAME,"jeg_meta_date")

    dateHasTime = False

    dateHasDateTimeAttribute = False
    dateTimeAttribute = "NULL"

    dateEndingSeparator = "NULL"
    dateStartSeparator = "NULL"
    dateTimeSeparator = "NULL"
    hourMinuteSeparator = "NULL"
    dayMonthYearSeparator = "/"
    monthNeedsMapper = False
    yearNeedsMapper = False
    dateMonthMapper = {}

    subtitle_locator = (By.CLASS_NAME ,"jeg_post_subtitle")

    image_locator = (By.CLASS_NAME ,'jeg_featured_img' )
    image_locator_internal = "NULL"
    image_locator_attribute = 'style'

    author_locator =  (By.CLASS_NAME ,'jeg_meta_author')
    author_locator_internal = (By.TAG_NAME, "a")
    author_locator_attribute = 'NULL'

    category_locator = 'NULL'
    category_locator_internal = 'NULL'

    addUrlCategories = False
    urlCategoryLowerBounds = []
    urlCategoryUpperBounds = []

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

    def get_main_image_url(self):
        if (self.image_locator == "NULL"):
            return "NULL"
        else:
            try:
                if (self.image_locator_internal == "NULL"):
                    imgElement = self.currentWrapper.find_element(*self.image_locator)
                else:
                    imgElement = self.currentWrapper.find_element(*self.image_locator).find_element(*self.image_locator_internal)
                print(imgElement.get_attribute(self.image_locator_attribute))
                return (imgElement.get_attribute(self.image_locator_attribute)).split('url("')[1].split('");')[0]
            except Exception as e:
                print(e)
                return "NULL"


"""
t = ESTUDOSNACIONAISScrapper(0)
data = t.scrap_article("https://www.estudosnacionais.com/30957/anvisa-registra-26-novos-obitos-por-vacinas-nas-ultimas-24-horas/")
t.append_article_to_txt(data)
t.driver.quit()
"""
