from news_crawler.base_scrapper import BaseScrapper
from selenium.webdriver.common.by import By

class UOLScrapper(BaseScrapper):
    def __init__(self,interface):
        if interface:
            super(UOLScrapper, self).__init__("firefox")
        else:
            super(UOLScrapper, self).__init__()


    text_locator = (By.CLASS_NAME,'text')
    scrapperSource = "UOL"
    title_locator = (By.XPATH, '//i[@ia-title=""]')
    main_wrapper_locator = (By.CLASS_NAME, 'article.article-wrapper.scroll-base.clearfix.collection-item.collection-first-item')
    date_locator = (By.CLASS_NAME, 'p-author.time')


    subtitle_locator = "NULL"
    image_locator = (By.CLASS_NAME,'pinit-wraper')
    author_locator =  (By.CLASS_NAME , 'p-author-local')
    author_locator_attribute = "NULL"
    category_locator = (By.CLASS_NAME,'title-name')
    video_locator = "NULL"  
    title_locator_internal = "NULL"
    
    undesirables = ['/videos','/colunas','/album','/reportagens-especiais', '/amp-stories', 'band.uol','stories','faq']
    
    dateHasDateTimeAttribute =True
    dateTimeAttribute = 'ia-date-publish'

    dateEndingSeparator = "Atu"
    dateHasTime = True
    dateTimeSeparator = " "
    hourMinuteSeparator = "h"
    dayMonthYearSeparator = "/"
    monthNeedsMapper = False

    addUrlCategories = True
    urlCategoryLowerBounds = [".br/"]
    urlCategoryUpperBounds = ["/2020/","/2021/"]

    manualCategories = ['coronavirus']

    image_locator_internal = (By.TAG_NAME, 'img')
    image_locator_attribute = 'src'

    def get_text(self):
        ret = ""
        texto = self.currentWrapper.find_element(*self.text_locator)
        trechos = texto.find_elements(By.TAG_NAME, 'p')
        for trecho in trechos:
            if (len(trecho.text) > 20):  #Necessario para reduzir chances de captar lixo
                try: #Necessario para conseguir identificar quotes e botar as aspas necessarias
                    trecho.find_element(By.TAG_NAME, 'cite')
                    ret+= "'"
                    ret+= (trecho.text)
                    ret+= "'" 
                    ret+= " " 
                except:
                    ret+= (trecho.text)
                    ret+= " " 
        return self.treat_text(ret)

u = UOLScrapper(0)
# data = u.scrap_article("https://noticias.uol.com.br/politica/ultimas-noticias/2021/06/05/abraham-e-arthur-weintraub-covid-19-estados-unidos.htm")
#data = u.scrap_article("https://noticias.uol.com.br/videos/2021/05/26/doria-recua-e-adia-flexibilizacao-em-sp-em-14-dias-apos-alta-nos-casos-de-covid-19.htm")
data = u.scrap_article("https://noticias.uol.com.br/politica/ultimas-noticias/2021/06/06/nao-havia-desejo-de-mudanca-diz-hajjar-que-rejeitou-ministerio-da-saude.htm")
u.append_article_to_txt(data)
u.driver.quit()

    # def get_main_video_url(self): 
    #     #Mas algumas URL da UOL tem video? Sim mas sao sempre trechos do fato (tipo senador X falando Y) e nao reportagens como no G1
    #     return "NULL"

    # def get_main_image_url(self):
    #     try:
    #         img = self.currentWrapper.find_element(*self.image_locator)
    #         return img.find_element(By.TAG_NAME,'img').get_attribute('src')
    #     except:
    #         return "NULL"


    # def get_category(self, articleUrl):
    #     #self.currentWrapper = self.driver.find_element(*self.main_wrapper_locator)


    #     #return [articleUrl.split('.br/')[1].split('/')[0]]
    #     time.sleep(20)
    #     return self.currentWrapper.find_element(*self.category_locator).text
    #     #return self.currentWrapper.find_element(*self.title_locator).text


    # def get_date(self):
    #     print("Usando data uol scrapper")
    #     rawDate = self.currentWrapper.find_element(*self.date_locator).text.split("Atu")[0]
    #     #rawDate = rawDate.split("Atu")
    #     #index = rawDate.find("Atu")
    #     #print(rawDate)
    #     #print(rawDate[:index])
    #     #rawDate, rawTime= rawDate[:index].split(" ")
    #     rawDate, rawTime= rawDate.split(" ")


    #     rawDay,rawMonth,rawYear = rawDate.split("/")
    #     rawHour, rawMinute = rawTime.split("h")

    #     data_publicacao = datetime( year=int(rawYear),
    #                                 month=int(rawMonth), 
    #                                 day=int(rawDay),
    #                                 hour=int(rawHour),
    #                                 minute=int(rawMinute))
    #     publication_date = data_publicacao.strftime('%Y-%m-%d %H:%M:%S')
    
    #     print("Pub date:" , publication_date)
    #     return publication_date 



# start = time.time()
# u = UOLScrapper(0)
# u.scrap_urls_file('UOL/URL/testeException.txt','historica_uol_continued')
# print("Total elapsed time:", time.time() -start)
# u.driver.quit()


    # def access_article(self, articleUrl):
    #     self.driver.get(articleUrl)

    # def get_main_wrapper(self, articleUrl):
    #     print("testeando abstract")
    #     self.currentWrapper = self.driver.find_element(*self.main_wrapper_locator)

    # def get_subtitle(self):
    #     return "NULL"

    # def get_title(self):
    #     return self.currentWrapper.find_element(*self.title_locator).text
    
    # def get_author(self):
    #     try:
    #         return self.currentWrapper.find_element(*self.author_locator).text
    #     except:
    #         return "NULL"


    # def scrap_article(self, articleUrl):
    #     for und in self.undesirables:
    #         if (und in articleUrl):
    #             raise UOLUndesirableException("Artigos " + und + " estão na lista de indesejados e não serão coletados(não são noticias)")
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
    #     file_path = os.getenv('PROJECT_DIR') + "/UOL/COLETA/" + features['source_name'].lower() + "_" + '_'.join(features['publication_date'].split('-')[0:2]) + ".txt"
    #     with open(file_path, mode='a', encoding='utf-8') as f:
    #         f.write(json.dumps(features, ensure_ascii=False) + '\n')
    
    # def html_file_name(self,url):
    #     return hashlib.sha1(url.encode()).hexdigest()+ ".html"

    # def save_html(self, features):
    #     file_path = os.getenv('PROJECT_DIR') + "/UOL/HTML/" + features['raw_file_name'] 
    #     with open(file_path, mode='w', encoding='utf-8') as f:
    #         f.write(self.driver.page_source)

    # def scrap_urls_file(self, fileName, taskName):
    #     LOG_FILENAME = os.getenv('PROJECT_DIR') + '/UOL/LOG/' + taskName + '.log'
    #     logging.basicConfig(filename=LOG_FILENAME, filemode ='w',level=logging.WARNING)
    #     count = 0
    #     latestTime = time.time()
    #     startTime = time.time()
    #     with open(fileName) as f:
    #         for url in f:
    #             print("Nova URL:", url)
    #             retry = 3
    #             while(retry > 0):
    #                 try:
    #                     urlDataPotentialPath = Path(os.getenv('PROJECT_DIR') + "/UOL/HTML/" + hashlib.sha1(url.encode()).hexdigest()+ ".html")
    #                     if(urlDataPotentialPath.is_file()):
    #                         print("Skipping artigo #", count)
    #                         count = count + 1
    #                         break
    #                     data = self.scrap_article(url)
    #                     self.append_article_to_txt(data)
    #                     mark = time.time()
    #                     print ("Scrapping artigo #", count, "Unitary time:" ,mark - latestTime , 'Elapsed time:', mark - startTime)
    #                     count = count + 1
    #                     latestTime = mark
    #                     retry = 3
    #                     break
    #                 except UOLUndesirableException as unde:
    #                     logging.warning(url + "\t" + str(type(unde)) + " : " + str(unde))
    #                     break
    #                 except InvalidSessionIdException as inval:
    #                     logging.exception(url)
    #                     super(UOLScrapper, self).__init__()
    #                     break
    #                 except Exception as e:
    #                     print ("\t Retrying", retry, "times" , url)
    #                     retry = retry - 1
    #                     time.sleep(5)
    #                     if retry == 0:
    #                         logging.exception(url)

# u = UOLScrapper(0)
# try:
#     data = u.scrap_article("https://noticias.uol.com.br/politica/ultimas-noticias/2021/05/22/aziz-bolsonaro-queria-que-eu-prendesse-wajngarten-e-acabasse-a-cpi.htm")
# except UOLVideoException:
#     print("Artigos 'video' do UOL são apenas links para o YT deles, não coletaremos.")
# else:    
#     u.append_article_to_txt(data)
# finally:
#     u.driver.close()
#     u.driver.quit()


#start = time.time()
#u = UOLScrapper(0)
#u.scrap_urls_file('UOL/URL/UOL_coronavirus_882_loads.txt','historica_uol_continued')
#print("Total elapsed time:", time.time() -start)
#u.driver.quit()










#Problemas: infinite load pages gerando timeout no driver.get() e causando fechamento do ddriver: 
    #Solucao big brain:
                        #except InvalidSessionIdException as inval:
                           # logging.exception(url)
                            #super(UOLScrapper, self).__init__()
                            #break
