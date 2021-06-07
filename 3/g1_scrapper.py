from news_crawler.base_scrapper import BaseScrapper
from selenium.webdriver.common.by import By

class G1Scrapper(BaseScrapper):
    def __init__(self,interface):
        if interface:
            super(G1Scrapper, self).__init__("firefox")
        else:
            super(G1Scrapper, self).__init__()

    text_locator = (By.CLASS_NAME,'content-text__container')
    scrapperSource = "G1"
    title_locator = (By.CLASS_NAME,'content-head__title')
    main_wrapper_locator = (By.CLASS_NAME, 'mc-body.theme')
    date_locator = (By.XPATH, '//time[@itemprop = "datePublished"]')

    subtitle_locator = (By.CLASS_NAME,'content-head__subtitle')
    image_locator = (By.TAG_NAME,'amp-img')
    author_locator =  (By.CLASS_NAME , 'content-publication-data__from')
    author_locator_attribute = 'title' 
    category_locator = (By.CLASS_NAME,'header-editoria--link.ellip-line')
    video_locator = (By.CLASS_NAME, "content-video__placeholder")
    title_locator_internal = "NULL"
    
    undesirables = ['/blog','/post','/especiais','/quiz']
    
    dateHasTime = True
    dateHasDateTimeAttribute = True
    dateTimeAttribute = 'datetime'

    dateEndingSeparator = "NULL"
    
    dateTimeSeparator = " "
    hourMinuteSeparator = "h"
    dayMonthYearSeparator = "/"
    monthNeedsMapper = False

    addUrlCategories = True
    urlCategoryLowerBounds = [".com/"]
    urlCategoryUpperBounds = ["/noticia"]

    manualCategories = ['coronavirus']

    image_locator_internal = "UNUSED"
    image_locator_attribute = "UNUSED"

    video_locator_internal = "UNUSED"
    video_locator_attribute = "UNUSED"

    text_locator_internal = "NULL"

    def get_main_video_url(self):
        block0 = self.currentWrapper.find_element(By.XPATH , '//div[@data-block-id="0"]')
        if (block0.get_attribute('data-block-type') == 'backstage-video'):
            return "globoplay.globo.com/v/" + block0.find_element(*self.video_locator).get_attribute('data-video-id') 
        else:
            return "NULL"
        pass

    def get_main_image_url(self):
        block0 = self.currentWrapper.find_element(By.XPATH , '//div[@data-block-id="0"]')
        if (block0.get_attribute('data-block-type') == 'backstage-photo'):
            return block0.find_element(*self.image_locator).get_attribute('src') 
        else:
            return "NULL"

G1 = G1Scrapper(0)
data = G1.scrap_article("https://g1.globo.com/bemestar/coronavirus/noticia/2021/04/25/covid-19-ja-matou-mais-brasileiros-em-4-meses-de-2021-do-que-em-todo-ano-de-2020.ghtml")
G1.append_article_to_txt(data)
G1.driver.quit()



    # def get_text(self):
    #     ret = ""
    #     trechos = self.currentWrapper.find_elements(*self.text_locator)
    #     for trecho in trechos:
    #         if (len(trecho.text) > 20): #Necessario por alguns jornalistas da globo fazem uso indevido da classe text__container para escrever substitulo
    #             ret += " " 
    #             ret+= (trecho.text)
    #     return ret




    # def __init__(self,interface):
    #     if interface:
    #         super(G1Scrapper, self).__init__("firefox")
    #     else:
    #         super(G1Scrapper, self).__init__()
    #     self.text_locator = (By.CLASS_NAME,'content-text__container')
    #     self.subtitle_locator = (By.CLASS_NAME,'content-head__subtitle')
    #     self.title_locator =(By.CLASS_NAME,'content-head__title')
    #     self.image_locator = (By.TAG_NAME,'amp-img')
    #     self.author_locator =  (By.CLASS_NAME , 'content-publication-data__from')
    #     self.category_locator =(By.CLASS_NAME,'header-editoria--link.ellip-line')
    #     self.main_wrapper_locator = (By.CLASS_NAME, 'mc-body.theme')
    #     self.date_locator = (By.XPATH, '//time[@itemprop = "datePublished"]')
    #     self.type = "noticia"
    #     self.fonte = "G1"
    #     self.video_locator = (By.CLASS_NAME, "content-video__placeholder")



    # def access_article(self, articleUrl):
    #     self.driver.get(articleUrl)



    # def get_subtitle(self):
    #     try:
    #         return self.currentWrapper.find_element(*self.subtitle_locator).text
    #     except:
    #         return "NULL"
        
    # def get_title(self):
    #     return self.currentWrapper.find_element(*self.title_locator).text
        
    # def get_author(self):
    #     try:
    #         return self.currentWrapper.find_element(*self.author_locator).get_attribute('title')
    #     except:
    #         return "NULL"

    # def get_category(self, articleUrl):
    #     #return articleUrl.split('/noticia/')[0].split('.com/')[1].split('/')
    #     return articleUrl.split('.com/')[1].split('/noticia')[0].split('/')

    # def get_main_wrapper(self, articleUrl):
    #     self.currentWrapper = self.driver.find_element(*self.main_wrapper_locator)

    # def get_date(self):
    #     rawDate,rawTime = self.currentWrapper.find_element(*self.date_locator).text.split(" ")
    #     rawDay,rawMonth,rawYear = rawDate.split("/")
    #     rawHour, rawMinute = rawTime.split("h")

    #     data_publicacao = datetime( year=int(rawYear),
    #                                 month=int(rawMonth), 
    #                                 day=int(rawDay),
    #                                 hour=int(rawHour),
    #                                 minute=int(rawMinute))
    #     publication_date = data_publicacao.strftime('%Y-%m-%d %H:%M:%S')

    #     return publication_date 
    


    # def scrap_article(self, articleUrl):
    #     self.access_article(articleUrl)
    #     time.sleep(2)
    #     self.get_main_wrapper(articleUrl)
    #     features = dict()
    #     features['url'] = articleUrl
    #     features['source_name'] = self.fonte
    #     features['title'] = self.get_title()
    #     features['subtitle'] = self.get_subtitle()
    #     features['publication_date'] = self.get_date()
    #     features['text_news'] = self.get_text()
    #     features['image_link'] = self.get_main_image_url()
    #     features['video_link'] = self.get_main_video_url()
    #     features['authors'] = self.get_author()
    #     features['categories'] = self.get_category(articleUrl)
    #     features['obtained_at'] = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    #     features['raw_file_name'] = self.html_file_name(articleUrl)
    #     self.save_html(features)
    #     return features

    # def append_article_to_txt(self, features):
    #     file_path = os.getenv('PROJECT_DIR') + "/G1/COLETA/" + features['source_name'].lower() + "_" + '_'.join(features['publication_date'].split('-')[0:2]) + ".txt"
    #     with open(file_path, mode='a', encoding='utf-8') as f:
    #         f.write(json.dumps(features, ensure_ascii=False) + '\n')
    
    # def html_file_name(self,url):
    #     return hashlib.sha1(url.encode()).hexdigest()+ ".html"

    # def save_html(self, features):
    #     file_path = os.getenv('PROJECT_DIR') + "/G1/HTML/" + features['raw_file_name'] 
    #     with open(file_path, mode='w', encoding='utf-8') as f:
    #         f.write(self.driver.page_source)

    # def scrap_urls_file(self, fileName, taskName):
    #     LOG_FILENAME = os.getenv('PROJECT_DIR') + '/G1/LOG/' + taskName + '.log'
    #     logging.basicConfig(filename=LOG_FILENAME, filemode ='w',level=logging.ERROR) 
    #     with open(fileName) as f:
    #         for url in f:
    #             retry = 3
    #             while(retry > 0):
    #                 try:
    #                     data = self.scrap_article(url)
    #                     self.append_article_to_txt(data)
    #                     retry = 3
    #                     break
    #                 except Exception as e:
    #                     retry = retry - 1
    #                     time.sleep(5)
    #                     if retry ==0:
    #                         logging.exception(url)
                    
# start = time.time()
# G1 = G1Scrapper(0)
# G1.scrap_urls_file('G1/URL/G1_bemestar_coronavirus_historica_may_24.txt','historica')
# print("Total elapsed time:", time.time() -start)
# G1.driver.quit()

        
    

#Imagem no topo
#G1.scrap_article("https://g1.globo.com/ciencia-e-saude/noticia/2020/02/03/chineses-que-sairam-de-cidade-em-quarentena-por-coronavirus-pedem-a-quem-ficou-para-cuidar-de-animais-de-estimacao.ghtml")

#Sem nada
#data = G1.scrap_article("https://g1.globo.com/bemestar/vacina/noticia/2021/04/25/brasil-aplicou-ao-menos-uma-dose-de-vacina-contra-covid-em-mais-de-29-milhoes-de-pessoas-aponta-consorcio-de-veiculos-de-imprensa.ghtml")
#G1.append_article_to_txt(data)
#G1.scrap_article("") 

#data = G1.scrap_article("https://g1.globo.com/bemestar/coronavirus/noticia/2021/05/21/numero-de-mortes-na-pandemia-pode-ser-ate-tres-vezes-maior-do-que-o-registrado-aponta-relatorio-da-oms.ghtml")
#G1.append_article_to_txt(data)
#G1.driver.close()

