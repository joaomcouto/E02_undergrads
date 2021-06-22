from news_crawler.base_scrapper import BaseScrapper
from selenium.webdriver.common.by import By

class ATROMBETAScrapper(BaseScrapper):
    def __init__(self,interface):
        if interface:
            super(ATROMBETAScrapper, self).__init__("firefox")
        else:
            super(ATROMBETAScrapper, self).__init__()

    scrapperSource = "ATROMBETA"

    main_wrapper_locator = (By.ID ,'content' )

    title_locator = (By.CLASS_NAME ,'entry-header' )
    title_locator_internal = (By.CLASS_NAME, 'entry-title')

    text_locator = (By.CLASS_NAME,'entry-content.clearfix' )
    text_locator_internal = (By.TAG_NAME, 'p')
    textUndesirables = []

    date_locator = (By.CLASS_NAME ,'entry-date.published' )
    date_locator_internal = "NULL"
    dateHasTime = True
    dateHasDateTimeAttribute = True
    dateTimeAttribute = 'datetime'
    dateStartSeparator = "NULL"
    dateEndingSeparator = "NULL"
    dateTimeSeparator = "NULL"
    hourMinuteSeparator = "NULL"
    dayMonthYearSeparator = "NULL"
    monthNeedsMapper = False
    yearNeedsMapper = False

    category_locator = "NULL"
    addUrlCategories = False
    urlCategoryLowerBounds = [".br/"]
    urlCategoryUpperBounds = ["/2020/","/2021/"]
    addTagsCategories = False
    tagsUndesirables = []

    subtitle_locator = "NULL"

    image_locator = (By.CLASS_NAME, 'attachment-colormag-featured-image.size-colormag-featured-image.wp-post-image' )
    image_locator_internal = "NULL"
    image_locator_attribute = 'src'

    author_locator = (By.CLASS_NAME, 'url.fn.n')
    author_locator_internal = 'NULL'
    author_locator_attribute = 'title'

    video_locator = "NULL"

    undesirables = []

    """
    MANUAL CATEGORIES (MUDAR DE ACORDO COM O EDITORAL SOBRE O QUAL O CRAWLING DE URLS FOR FEITO)
                Necessario pois no inicio da pandemia por exemplo no g1, noticias de covid tem apenas a categoria "ciencia-e-saude"
                Alem disso, outro exemplo, noticias de politica relacionadas a covid frequentente recebem apenas a categoria "politica"
    """
    manualCategories = []


t = ATROMBETAScrapper(0)
#data = t.scrap_article("https://atrombetanews.com.br/2020/03/29/todos-infectados-pelo-covid-19-estao-curados-em-blumenau-santa-catarina-dentre-eles-um-idoso-de-72-anos/?fbclid=IwAR1ePn7ka554HfNuqv8jTCVJFoKUqASAo4XGIMKGdnvIIhSiJezMWfU65q0")
#data = t.scrap_article("https://atrombetanews.com.br/2021/03/12/medicos-europeus-pedem-uso-urgente-da-ivermectina-no-tratamento-contra-a-covid-19-video/")
data = t.scrap_article("https://atrombetanews.com.br/2021/02/24/vacinas-causam-600-novos-casos-de-doencas-oculares-e-deixam-5-pessoas-cegas-de-acordo-com-o-governo-do-reino-unido/")
t.append_article_to_txt(data)
data2 = t.scrap_article("https://atrombetanews.com.br/2021/03/12/medicos-europeus-pedem-uso-urgente-da-ivermectina-no-tratamento-contra-a-covid-19-video")
t.append_article_to_txt(data2)

#Isadora
data3 = t.scrap_article("http://www.atrombetanews.com.br/2020/03/29/todos-infectados-pelo-covid-19-estao-curados-em-blumenau-santa-catarina-dentre-eles-um-idoso-de-72-anos/?fbclid=IwAR1ePn7ka554HfNuqv8jTCVJFoKUqASAo4XGIMKGdnvIIhSiJezMWfU65q0")
t.append_article_to_txt(data3)

t.driver.quit()
