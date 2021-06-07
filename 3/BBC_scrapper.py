from news_crawler.base_scrapper import BaseScrapper
from selenium.webdriver.common.by import By

class BBCScrapper(BaseScrapper):
    def __init__(self,interface):
        if interface:
            super(BBCScrapper, self).__init__("firefox")
        else:
            super(BBCScrapper, self).__init__()

    text_locator = (By.CLASS_NAME,'bbc-19j92fr.e57qer20')
    scrapperSource = "BBC"
    title_locator = (By.CLASS_NAME,'bbc-1lsgtu3.e1yj3cbb0')
    main_wrapper_locator = (By.TAG_NAME, 'main')
    #date_locator = (By.CLASS_NAME, 'e1j2237y6.bbc-q4ibpr.e57qer20')
    date_locator = (By.CLASS_NAME, 'bbc-14xtggo.e4zesg50')

    subtitle_locator = "NULL"
    image_locator = (By.CLASS_NAME,'bbc-1qdcvv9.e6bmn90') 
    author_locator =  (By.CLASS_NAME , 'e1j2237y5.bbc-q4ibpr.e57qer20') 
    author_locator_attribute = "NULL"
    category_locator = "NULL"
    video_locator = "NULL"  
    title_locator_internal = "NULL"
    
    dateHasDateTimeAttribute = True
    dateTimeAttribute = 'datetime'

    dateEndingSeparator = "\n"
    dateHasTime = False
    dateTimeSeparator = "NULL"
    hourMinuteSeparator = "NULL"
    dayMonthYearSeparator = " "
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

    addUrlCategories = True
    urlCategoryLowerBounds = ["portuguese/"]
    urlCategoryUpperBounds = ["-"]
    manualCategories = ['coronavirus']

    image_locator_internal = "NULL"
    image_locator_attribute = "NULL"

    text_locator_internal = (By.CLASS_NAME, 'bbc-bm53ic.e1cc2ql70')
    textUndesirables = ["Inscreva-se no nosso canal!"]

    def get_main_image_url(self):
        images = self.currentWrapper.find_elements(*self.image_locator)
        for im in images:       
            try: #Necessario para conseguir diferenciar a imagem principal de outras imagens na noticia
                im.find_element(By.CLASS_NAME, 'lazyload-wrapper')
            except:
                return im.find_element(By.TAG_NAME,'img').get_attribute('src')
    
        
b = BBCScrapper(0)
#data = b.scrap_article("https://www.bbc.com/portuguese/internacional-57143976")
#data = b.scrap_article("https://www.bbc.com/portuguese/brasil-51713943")
data = b.scrap_article("https://www.bbc.com/portuguese/internacional-56503711")
b.append_article_to_txt(data)
b.driver.close()




    # def get_author(self): #Algumas noticias na BBC nao tem autor vide https://www.bbc.com/portuguese/internacional-57143976
    #     try:
    #         return self.currentWrapper.find_element(*self.author_locator).text.replace('\n', ' ')
    #     except:
    #         return "NULL"



    # def get_text(self):
    #     ret = ""
    #     trechos = self.currentWrapper.find_elements(*self.text_locator)        
    #     for trecho in trechos:
    #         #print("Trecho:", trecho.text , '\n')
    #         try: 
    #             #Necessario para jogar fora os substitulos ao longo da materia e tambem listagens para outras reportagens
    #             #Exemplo de materia com subtitulo e listagem: https://www.bbc.com/portuguese/geral-53681929
    #             para = trecho.find_element(By.TAG_NAME, 'p')

    #             if (len(para.text) > 15):  #Necessario para reduzir chances de captar lixo
    #                 if("Inscreva-se no nosso canal!" in para.text):
    #                     continue
    #                 ret+= (para.text)
    #                 ret+= " " 
    #                 #print(para.text)
    #                 #print(len(para.text), "\n")
    #         except:
    #             #print("Não tem a tag p, indicativo de substitulo, listagem ou propaganda do canal do BBC")
    #             continue
    #     return ret



# class BBCScrapper(BaseCrawler):
#     def __init__(self,interface):
#         if interface:
#             super(BBCScrapper, self).__init__("firefox")
#         else:
#             super(BBCScrapper, self).__init__()

#         self.text_locator = (By.CLASS_NAME,'bbc-19j92fr.e57qer20')
        #self.subtitle_locator = (By.CLASS_NAME,'content-head__subtitle') #BBC não tem subtitulo

        # self.title_locator =(By.CLASS_NAME,'bbc-1lsgtu3.e1yj3cbb0')

        # self.image_locator = (By.CLASS_NAME,'bbc-1qdcvv9.e6bmn90') #O difenrenciar da main image vai ser a nao presenca da classe lazyloader
        # self.author_locator =  (By.CLASS_NAME , 'e1j2237y6.bbc-q4ibpr.e57qer20') #Algumas noticias na BBC nao tem autor

        #self.category_locator =(By.CLASS_NAME,'title-name') 
            #Noticias na BBC não tem categoria
            #Quase todas as noticiais sao 'geral' , 'internacional' ou 'brasil'
                # -> Coletarei isso da URL
            #Assim para saber a categoria DE VERDADE é necessario na hora do scrapping, ver de qual coleta de "editorial" a URL esta vindo
        

        # self.main_wrapper_locator = (By.TAG_NAME, 'main')
        # self.date_locator = (By.CLASS_NAME, 'e1j2237y6.bbc-q4ibpr.e57qer20')
        # self.type = "noticia"
        # self.fonte = "BBC"
        #self.video_locator = (By.CLASS_NAME, "content-video__placeholder") #BBC não tem vídeo 



    # def access_article(self, articleUrl):
    #     self.driver.get(articleUrl)



    # def get_subtitle(self):
    #     return "NULL"

    # def get_title(self):
    #     return self.currentWrapper.find_element(*self.title_locator).text
        



    # def get_category(self, articleUrl):
    #     return [articleUrl.split('portuguese/')[1].split('-')[0]]
    
    # def get_main_wrapper(self, articleUrl):
    #     self.currentWrapper = self.driver.find_element(*self.main_wrapper_locator)

    # def get_date(self):
    #     rawDate = self.currentWrapper.find_element(*self.date_locator).text
    #     #print(rawDate + "\n")
    #     rawDate = rawDate.split('\n')[0]
    #     #print(rawDate)
    #     mapper = {
    #             'janeiro': 1,
    #             'fevereiro': 2,
    #             'março': 3,
    #             'abril': 4,
    #             'maio': 5,
    #             'junho': 6,
    #             'julho': 7,
    #             'agosto': 8,
    #             'setembro': 9,
    #             'outubro': 10,
    #             'novembro': 11,
    #             'dezembro': 12
    #         }
    #     rawDay,rawMonth,rawYear = rawDate.split(" ")
    #     rawMonth = mapper[rawMonth]

    #     data_publicacao = datetime( year=int(rawYear),
    #                                 month=int(rawMonth), 
    #                                 day=int(rawDay))
    #     publication_date = data_publicacao.strftime('%Y-%m-%d %H:%M:%S')

    #     return publication_date 
  
    # def get_main_video_url(self):
    #     return "NULL"



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
    #     file_path = os.getenv('PROJECT_DIR') + "/BBC/COLETA/" + features['source_name'].lower() + "_" + '_'.join(features['publication_date'].split('-')[0:2]) + ".txt"
    #     with open(file_path, mode='a', encoding='utf-8') as f:
    #         f.write(json.dumps(features, ensure_ascii=False) + '\n')
    
    # def html_file_name(self,url):
    #     return hashlib.sha1(url.encode()).hexdigest()+ ".html"

    # def save_html(self, features):
    #     file_path = os.getenv('PROJECT_DIR') + "/BBC/HTML/" + features['raw_file_name'] 
    #     with open(file_path, mode='w', encoding='utf-8') as f:
    #         f.write(self.driver.page_source)

    # def scrap_urls_file(self, fileName, taskName):
    #     LOG_FILENAME = os.getenv('PROJECT_DIR') + '/BBC/LOG/' + taskName + '.log'
    #     logging.basicConfig(filename=LOG_FILENAME, filemode ='w',level=logging.WARNING)
    #     count = 0
    #     latestTime = time.time()
    #     startTime = time.time()
    #     with open(fileName) as f:
    #         for lineNumber,url in enumerate(f):
    #             url = url.rstrip()
    #             print("Nova URL:", url)
    #             retry = 3
    #             while(retry > 0):
    #                 try:
    #                     urlDataPotentialPath = Path(os.getenv('PROJECT_DIR') + "/BBC/HTML/" + hashlib.sha1(url.encode()).hexdigest()+ ".html")
    #                     if(urlDataPotentialPath.is_file()):
    #                         print("Skipping artigo #", lineNumber)
    #                         break
    #                     data = self.scrap_article(url)
    #                     self.append_article_to_txt(data)
    #                     mark = time.time()
    #                     print ("Scrapping artigo #", lineNumber, "Unitary time:" ,mark - latestTime , 'Elapsed time:', mark - startTime)
    #                     latestTime = mark
    #                     retry = 3
    #                     break
    #                 #except UOLUndesirableException as unde:
    #                 #    logging.warning(url + "\t" + str(type(unde)) + " : " + str(unde))
    #                 #    break
    #                 except InvalidSessionIdException as inval:
    #                     logging.exception(url)
    #                     super(BBCScrapper, self).__init__()
    #                     break
    #                 except Exception as e:
    #                     print ("\t Retrying", retry, "times" , url)
    #                     retry = retry - 1
    #                     time.sleep(5)
    #                     if retry == 0:
    #                         logging.exception(url)



#b = BBCScrapper(0)
#b.scrap_urls_file('BBC/URL/BCC_topics_c340q430z4vt_historia_april_17.txt','historica_BBC')
#b.driver.quit()


#u.scrap_urls_file('UOL/URL/UOL_coronavirus_882_loads.txt','historica_uol_continued')
##print("Total elapsed time:", time.time() -start)
#u.driver.quit()


#https://www.bbc.com/portuguese/topics/c340q430z4vt





"""
Problema: eliminar do texto o link "Clique para assinar o canal da BBC News Brasil no YouTube" colocado em ALGUMAS reportagens, que usa a mesma classe que os paragrafos
    Solução: encontrar dentro de cada item da classe pela tag 'p' presente em todos os paragrafos reais, a propaganda não tem

Problema: eliminar subtitulos:
    Solução: encontrar dentro de cada item da classe pela tag 'p' presente em todos os paragrafos reais, os subtitulos não tem

Problema: eliminar do texto o link "Já assistiu aos nossos novos vídeos no YouTube? Inscreva-se no nosso canal!" que tem em todas as reportagens
    Solução: verificar todas as strings para ver se são essa antes de inserir no dicionario.. necessario pois a estrutura do HTML dessa propagando é identica à de um paragrafo de texto qualquer...
            inclusive muitos dos paragrafos normais tambem tem link então isso não é uma diferenciação valida ...
            Alem disso eliminar o ultimo match não basta pois existem matches aleatorios com paragrafos vazio logo depois dessa propaganda, veja:
                Trecho: Já assistiu aos nossos novos vídeos no YouTube? Inscreva-se no nosso canal! 

                Trecho:  

                Trecho:  

                Trecho:  

https://www.bbc.com/portuguese/geral-53681929
Problema: string "Escute esta reportagem em áudio neste link."
    Solução: não existe pois isso é algo manualmente inserior pelo reporter.. apenas um paragrafo com um texto
"""



#https://www.bbc.com/portuguese/brasil-51713943



