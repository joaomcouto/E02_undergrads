from COLETORES.base_scrapper import BaseScrapper
from selenium.webdriver.common.by import By

class BBCScrapper(BaseScrapper):
    def __init__(self,interface):
        if interface:
            super(BBCScrapper, self).__init__("firefox")
        else:
            super(BBCScrapper, self).__init__()

    scrapperSource = "BBC"

    main_wrapper_locator = (By.TAG_NAME, 'main')#OBRIGATORIO NÃO NULL

    title_locator = (By.CLASS_NAME,'bbc-1lsgtu3.e1yj3cbb0') #OBRIGATORIO NÃO NULL
    title_locator_internal = "NULL" #OBRIGATORIO MAS PODE SER "NULL"/VAZIO

    text_locator = (By.CLASS_NAME,'bbc-19j92fr.e57qer20')
    text_locator_internal = (By.CLASS_NAME, 'bbc-bm53ic.e1cc2ql70')
    textUndesirables = ["Inscreva-se no nosso canal!"]

    date_locator = (By.CLASS_NAME, 'bbc-14xtggo.e4zesg50')
    date_locator_internal = "NULL" #OBRIGATORIO MAS PODE SER "NULL"/VAZIO
    dateHasTime = False
    dateHasDateTimeAttribute = True
    dateTimeAttribute = 'datetime'
    dateStartSeparator = "NULL" #PODE SER APAGADO SE O BOOL OBRIGATORIO ACIMA MAIS PROXIMO FOR TRUE
    dateEndingSeparator = "\n"
    dateTimeSeparator = "NULL" #PODE SER APAGADO SE O BOOL OBRIGATORIO ACIMA MAIS PROXIMO FOR TRUE
    hourMinuteSeparator = "NULL" #PODE SER APAGADO SE O BOOL OBRIGATORIO ACIMA MAIS PROXIMO FOR TRUE
    dayMonthYearSeparator = "NULL" #PODE SER APAGADO SE O BOOL OBRIGATORIO ACIMA MAIS PROXIMO FOR TRUE
    monthNeedsMapper = False #PODE SER APAGADO SE O BOOL OBRIGATORIO ACIMA MAIS PROXIMO FOR TRUE
    dateMonthMapper = {} #PODE SER APAGADO SE O BOOL OBRIGATORIO ACIMA MAIS PROXIMO FOR TRUE
    yearNeedsMapper = False #PODE SER APAGADO SE O BOOL OBRIGATORIO ACIMA MAIS PROXIMO FOR TRUE
    dateYearMapper = {} #PODE SER APAGADO SE O BOOL OBRIGATORIO ACIMA MAIS PROXIMO FOR TRUE

    ####Parametros abaixo desta linha são referentes a métodos que podem retornar "NULL" no caso de de erro. Acima desta linha, erros em métodos resultam em excessões que devem ser tratadas apenas para logging.
    ### Isso significa que uma coleta é considerada sucesso mesmo que os campos categories, subtitles, image_url, video_url sejam "NULL" mesmo que por motivo de excessão.

    category_locator = "NULL"
    category_locator_internal = 'NULL' #PODE SER APAGADO SE O OBRIGATORIO ACIMA MAIS PROXIMO FOR "NULL"
    addUrlCategories = True
    urlCategoryLowerBounds = ["portuguese/"]
    urlCategoryUpperBounds = ["-"]
    manualCategories = ['coronavirus']

    
    addTagsCategories = False #OBRIGATORIO NÃO NULL
    tags_categories_locator = "NULL"#PODE SER APAGADO SE O BOOL OBRIGATORIO ACIMA MAIS PROXIMO FOR FALSE
    tags_categories_locator_internal = "NULL" #PODE SER APAGADO SE O BOOL OBRIGATORIO ACIMA MAIS PROXIMO FOR FALSE
    tagsUndesirables = [] #OBRIGATORIO MAS PODE SER "NULL"/VAZIO

    subtitle_locator = "NULL"

    image_locator = (By.CLASS_NAME,'bbc-1qdcvv9.e6bmn90')
    image_locator_internal = "NULL" #PODE SER APAGADO SE O OBRIGATORIO ACIMA MAIS PROXIMO FOR "NULL"
    image_locator_attribute = "NULL" #PODE SER APAGADO SE O OBRIGATORIO ACIMA MAIS PROXIMO FOR "NULL"

    author_locator =  (By.CLASS_NAME , 'e1j2237y5.bbc-q4ibpr.e57qer20')
    author_locator_internal = 'NULL' #PODE SER APAGADO SE O OBRIGATORIO ACIMA MAIS PROXIMO FOR "NULL"
    author_locator_attribute = "NULL"

    video_locator = "NULL"    
    title_locator_internal = "NULL"
    video_locator_attribute = 'NULL'#PODE SER APAGADO SE O OBRIGATORIO ACIMA MAIS PROXIMO FOR "NULL"

    undesirables = [] #OBRIGATORIO MAS PODE SER "NULL"/VAZIO



    def get_main_image_url(self):
        images = self.currentWrapper.find_elements(*self.image_locator)
        for im in images:
            try: #Necessario para conseguir diferenciar a imagem principal de outras imagens na noticia
                im.find_element(By.CLASS_NAME, 'lazyload-wrapper')
            except:
                return im.find_element(By.TAG_NAME,'img').get_attribute('src')


"""
b = BBCScrapper(0)
#data = b.scrap_article("https://www.bbc.com/portuguese/internacional-57143976")
#data = b.scrap_article("https://www.bbc.com/portuguese/brasil-51713943")
data = b.scrap_article("https://www.bbc.com/portuguese/internacional-56503711")
b.append_article_to_txt(data)
b.driver.close()
"""

#b = BBCScrapper(0)
#b.scrap_urls_file('BBC/URL/BCC_topics_c340q430z4vt_historia_april_17.txt','historica_BBC')
#b.driver.quit()


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
