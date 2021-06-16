from news_crawler.base_scrapper import BaseScrapper
from selenium.webdriver.common.by import By

class LUISCARDOSOScrapper(BaseScrapper):
    def __init__(self, interface):
        if interface:
            super(LUISCARDOSOScrapper, self).__init__("firefox")
        else:
            super(LUISCARDOSOScrapper, self).__init__()

    main_wrapper_locator = (By.CLASS_NAME ,"post-entry" )

    text_locator = (By.CLASS_NAME,'post-content')
    text_locator_internal = (By.TAG_NAME, 'p')
    textUndesirables = ['Acompanhe o Blog do Luis Cardoso também pelo']

    scrapperSource = "LUISCARDOSO"
    title_locator = (By.CLASS_NAME ,'post-title' )
    title_locator_internal = "NULL"

    date_locator = (By.CLASS_NAME ,'post-date' )
    date_locator_internal = (By.TAG_NAME, 'time')

    dateHasTime = True

    dateHasDateTimeAttribute = False
    dateTimeAttribute = 'NULL'

    dateEndingSeparator = ""
    dateTimeSeparator = " às "
    hourMinuteSeparator = ":"
    dayMonthYearSeparator = " de "
    monthNeedsMapper = True
    dateMonthMapper = {
		'Jan': 1,
		'Fev': 2,
		'Mar': 3,
		'Abr': 4,
		'Maio': 5,
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
        '26': 2026,
        '25': 2025,
        '24': 2024,
        '23': 2023,
        '22': 2022,
        '21': 2021,
        '20': 2020,
        '19': 2019,
        '18': 2018,
        '17': 2017,
        '16': 2016,
        '15': 2015,
        '14': 2014,
        '13': 2013,
        '12': 2012,
        '11': 2011,
        '10': 2010
    }

    def get_date(self):
        if(self.date_locator_internal == "NULL"):
            dateElement =self.currentWrapper.find_element(*self.date_locator)
        else:
            dateElement =self.currentWrapper.find_element(*self.date_locator).find_element(*self.date_locator_internal)

        if(self.dateHasDateTimeAttribute):
            dateText =dateElement.get_attribute(self.dateTimeAttribute)
            if(self.dateHasTime):
                fmt ="%Y-%m-%dT%H:%M:%S"
                try:
                    data_publicacao = datetime.strptime(dateText, fmt)
                except ValueError as v:
                    if len(v.args) > 0 and v.args[0].startswith('unconverted data remains: '):
                        dateText = dateText[:-(len(v.args[0]) - 26)]
                        data_publicacao = datetime.strptime(dateText, fmt)
                    else:
                        raise
                publication_date = data_publicacao.strftime('%Y-%m-%d %H:%M:%S')
                return publication_date
            else:
                fmt ="%Y-%m-%d"
                try:
                    data_publicacao = datetime.strptime(dateText, fmt)
                except ValueError as v:
                    if len(v.args) > 0 and v.args[0].startswith('unconverted data remains: '):
                        dateText = dateText[:-(len(v.args[0]) - 26)]
                        data_publicacao = datetime.strptime(dateText, fmt)
                    else:
                        raise
                publication_date = data_publicacao.strftime('%Y-%m-%d %H:%M:%S')
                return publication_date

        else:
            dateText = dateElement.text.split(self.dateEndingSeparator)[0]
            #print(dateText)



            if(self.dateHasTime):
                #print(dateText)
                dateText, timeText = dateText.split(self.dateTimeSeparator)
                publicationHour, publicationMinute = timeText.split(self.hourMinuteSeparator)

            publicationDay,publicationMonth,publicationYear = dateText.split(self.dayMonthYearSeparator)

            if(self.monthNeedsMapper):
                publicationMonth = self.dateMonthMapper[publicationMonth]

            if(self.yearNeedsMapper):
                publicationYear = self.dateYearMapper[publicationYear]

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


    subtitle_locator = "NULL"

    image_locator = (By.CLASS_NAME ,'post-content' )
    image_locator_internal = (By.TAG_NAME, "img")
    image_locator_attribute = 'src'

    #author_locator =  (By.XPATH ,'//span[@style="color: rgb(159, 159, 223);"]' )
    author_locator =  (By.CLASS_NAME ,'author vcard')
    author_locator_internal = (By.TAG_NAME ,'a')
    author_locator_attribute = 'NULL'

    category_locator = (By.XPATH ,"//div[@class='post-info']/a[@rel='category tag']")  # TEMPORARIO PENDENTE IMPLEMENTACAO DE TAGS
    category_locator_internal = 'NULL'
    addUrlCategories = False
    urlCategoryLowerBounds = []
    urlCategoryUpperBounds = []

    addTagsCategories = False
    tags_categories_locator = (By.CLASS_NAME ,'td-tags.td-post-small-box.clearfix')
    tags_categories_locator_internal = (By.TAG_NAME ,'li')
    tagsUndesirables = ["TAGS"]


    video_locator = "NULL"#(By.CLASS_NAME ,"wp-block-video")
    video_locator_internal = "NULL"#(By.TAG_NAME ,"video")
    video_locator_attribute = "NULL"#"src"

    undesirables = []


    """
    MANUAL CATEGORIES (MUDAR DE ACORDO COM O EDITORAL SOBRE O QUAL O CRAWLING DE URLS FOR FEITO)
                Necessario pois no inicio da pandemia por exemplo no g1, noticias de covid tem apenas a categoria "ciencia-e-saude"
                Alem disso, outro exemplo, noticias de politica relacionadas a covid frequentente recebem apenas a categoria "politica"
    """
    manualCategories = []



q = LUISCARDOSOScrapper(0)
data = q.scrap_article("https://luiscardoso.com.br/saude/2020/02/alerta-hospital-sao-domingos-registra-caso-de-crianca-com-coronavirus-em-sao-luis/?fbclid=IwAR3ZsGnHzAs_XsU3VL8sfdCF4VkYmQYsnHKSqIGbJEuNoictWj_7_f6uCpY")
q.append_article_to_txt(data)
q.driver.quit()
