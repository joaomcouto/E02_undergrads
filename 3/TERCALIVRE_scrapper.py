from news_crawler.base_scrapper import BaseScrapper
from selenium.webdriver.common.by import By
from datetime import datetime
class TERCALIVREScrapper(BaseScrapper):
    def __init__(self,interface):
        if interface:
            super(TERCALIVREScrapper, self).__init__("firefox")
        else:
            super(TERCALIVREScrapper, self).__init__()

    main_wrapper_locator = (By.CLASS_NAME ,'col-lg-9.col-md-9.col-mod-single.col-mod-main' )

    text_locator = (By.CLASS_NAME,'entry-content.herald-entry-content')
    text_locator_internal = (By.TAG_NAME, 'p')
    textUndesirables = []

    scrapperSource = "TERCALIVRE"
    title_locator = (By.CLASS_NAME ,'entry-title.h1' )
    title_locator_internal = "NULL"
    
    date_locator = (By.CLASS_NAME ,'updated' )
    date_locator_internal = "NULL"

    dateHasTime = True

    dateHasDateTimeAttribute = False
    dateTimeAttribute = 'NULL'

    dateEndingSeparator = "NULL"
    dateTimeSeparator = "NULL"
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

    subtitle_locator = "NULL"

    image_locator = (By.CLASS_NAME ,'herald-post-thumbnail.herald-post-thumbnail-single' )
    image_locator_internal = (By.TAG_NAME, "img")
    image_locator_attribute = 'src'

    #author_locator =  (By.XPATH ,'//span[@style="color: rgb(159, 159, 223);"]' )
    author_locator =  (By.CLASS_NAME ,'herald-author-name')
    author_locator_internal = "NULL"
    author_locator_attribute = 'NULL'

    category_locator = 'NULL' 
    category_locator_internal = 'NULL'
    addUrlCategories = False
    urlCategoryLowerBounds = []
    urlCategoryUpperBounds = []

    addTagsCategories = True
    tags_categories_locator = (By.CLASS_NAME ,'meta-tags')
    tags_categories_locator_internal = (By.TAG_NAME ,'a')
    tagsUndesirables = []


    video_locator = "NULL"
    video_locator_internal = "NULL"
    video_locator_attribute = "NULL"
    
    undesirables = []
    

    """
    MANUAL CATEGORIES (MUDAR DE ACORDO COM O EDITORAL SOBRE O QUAL O CRAWLING DE URLS FOR FEITO)
                Necessario pois no inicio da pandemia por exemplo no g1, noticias de covid tem apenas a categoria "ciencia-e-saude"
                Alem disso, outro exemplo, noticias de politica relacionadas a covid frequentente recebem apenas a categoria "politica"
    """
    manualCategories = []
    def get_date(self):
        if(self.date_locator_internal == "NULL"):
            dateElement =self.currentWrapper.find_element(*self.date_locator)
        else:
            dateElement =self.currentWrapper.find_element(*self.date_locator).find_element(*self.date_locator_internal)

        dateText = dateElement.text.split(self.dateEndingSeparator)[0]
        #print(dateText)

        if(self.dateHasTime):
            #print(dateText)
            timeText = dateText[-5:]
            dateText = dateText[:-6]

            publicationHour, publicationMinute = timeText.split(self.hourMinuteSeparator)

        publicationDay,publicationMonth,publicationYear = dateText.split(self.dayMonthYearSeparator)

        if(self.monthNeedsMapper):
            publicationMonth = self.dateMonthMapper[publicationMonth]

        if(self.dateHasTime):
            data_publicacao = datetime( year=int(publicationYear),
                                    month=int(publicationMonth), 
                                    day=int(publicationDay),
                                    hour=int(publicationHour),
                                    minute=int(publicationMinute))
        else:
            data_publicacao = datetime( year=int(publicationYear),
                                    month=int(publicationMonth), 
                                    day=int(publicationDay))

        publication_date = data_publicacao.strftime('%Y-%m-%d %H:%M:%S')
        return publication_date 


t = TERCALIVREScrapper(0)
data = t.scrap_article("https://tercalivre.com.br/alexandre-de-moraes-retira-sigilo-do-inquerito-dos-supostos-atos-antidemocraticos/")
t.append_article_to_txt(data)
t.driver.quit()