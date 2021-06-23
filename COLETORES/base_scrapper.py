'''
DESCRIPTION:
Este modulo define a classe base "BaseScrapper" a ser utilizada em todos scrappers desenvolvidos para a coleta de noticias e/ou fact-checking neste projeto

Esta classe semi-abstrata define uma serie de métodos "padrão" que buscam ser robustos o suficiente para conseguir coletar dados de quaisquer sites de noticia ou verificação de fatos

O objetivo é permitir que um scrapper para um site inédito possa ser desenvolvido em poucas linhas de código, bastando definir os parametros deste BaseScrapper

Na eventualidade da lógica de um método dessa classe não se encaixar com a coleta de um campo de um dado site, basta redefinir o método na classe scrapper que o herda.
    Observamos que os métodos definidos aqui servem de base para a criação de métodos customizados nestes casos, e que, na maioria dos casos, basta trocar uma ou duas linhas sobre como eles funcionam


NOÇÕES BÁSICAS?

A ideia básica de uso dos métodos aqui presentes é a definição de 3 níveis de finders do Selenium, 1 compartilhado por todos os métodos e 2 especificos de cada método
    main_wrapper_locator, obrigatorio
    x_locator, obrigatorio
    x_locator_internal, opcional

Com esses parametros/finders definidos, os métodos então buscam dentro de main_wrapper o elemento x_locator e, 
    se o x_locator_internal for diferente de "NULL", buscam por x_locator_internal dentro do elemento que foi encontrado por x_locator

Assim temos: 

main_wrapper_locator finder para elemento HTML UNICO NA PAGINA mais interno que contém todas a informações que se deseja coletar com o Scrapper.

x_locator deve ser IDEALMENTE o finder para os elementos HTML dentro do main_wrapper que contenham APENAS o dado que um certo método busca coletar
    Se x_locator não for o suficiente para isolar apenas os elementos que o método busca coletar, utilizamos o x_locator_internal

x_locator_internal deve então conter o finder para os elementos HTML dentro de x_locator que contenham APENAS o dado que um dado método busca coletar

Observamos que a probabilidade de que estes dois níveis de filtro sejam insuficientes, considerando todas as formas que temos de encontrar elementos no selenium, é pragmaticamente nula

Uma vez isolados os elementos duas coisas podem acontecer:
    1 - O método vai extrair o texto .text dos elementos isolados
    2 - Podemos definir o parametro x_locator_attribute, neste caso, o método vai extrair o valor do atributo x_locator_attribute dos elementos HTML isolados


EXEMPLO PRATICO SIMPLES: 
    Preparando um scrapper para extrair o autor do site https://revistaoeste.com/brasil/ (USO DE X_LOCATOR E .TEXT APENAS)

    Temos o site de baixa credibilidade https://revistaoeste.com/
    E vamos extrair os dados da noticia https://revistaoeste.com/brasil/novo-lote-de-insumos-sera-enviado-a-fiocruz-no-dia-21-diz-secretario/
    Vamos primeiro encontrar o main-wrapper que contenha todos os elementos:
    Clicamos com o botão direito sobre alguma parte da noticia por exemplo, o titulo, e clicamos em "inspect" para ver o código fonte da página
        Navegamos "pra cima" na arvore do HTML até encontrar o primeiro elemento com algum atributo único que contenha tudo da noticia
        Encontramos inicialmente o elemento com várias classes, entre elas a "opened", serve? Sim, se clicarmos CTRL+F e pesquisarmos por "opened" vemos que é o único elemento HTML na página com essa classe
        Assim, setamos, na classe de nosso scrapper, o parametro:
            ain_wrapper_locator = (By.CLASS_NAME ,'opened' )

    Para este exemplo vamos extrair apenas o autor
    Agora vamos fazer o mesmo processo para achar o autor
        Clicamos com o botão direito sobre o titulo, e clicamos em "inspect" para ver o código fonte da página
        Vemos que a classe dele tem as classes 'url', 'fn' e 'n', serve? Sim! Clicamos Ctrl+F e pesquisamos por 'url fn n' e vemos que essa combinação de classes é unica dentre os elementos dentro do nosso main_wrapper
        Assim, setamos na classe de nosso scrapper, o parametro:
            author_locator =  (By.CLASS_NAME ,'url.fn.n')
        Veja, essa classe já isola a classe que contem o texto com o autor da noticia..

    Pronto! Com esse simple processo nosso scrapper está pronto para extrair autores do site https://revistaoeste.com/brasil/
    Basta repetir o mesmo processo com os outros parametros e em cerca de 20 minutos, o scrapper completo estará pronto.





EXEMPLO PRÁTICO MEDIO: preparando um scrapper para extrair o titulo do site https://atrombetanews.com.br/ (USO DE X_LOCATOR + X_LOCATOR_INTERNAL + .TEXT (sem x_locator_attribute))

    Temos o site de baixa credibilidade https://atrombetanews.com.br/
    E vamos extrair os dados da noticia https://atrombetanews.com.br/2020/09/25/com-slogan-tratamento-precoce-e-vida-governo-bolsonaro-planeja-dia-d-contra-covid-em-03-de-outubro-com-kit-com-hidroxicloroquina-cloroquina-azitromicina-ivermec/
    Vamos primeiro encontrar o main-wrapper que contenha todos os elementos:
    Clicamos com o botão direito sobre alguma parte da noticia por exemplo, o titulo, e clicamos em "inspect" para ver o código fonte da página
        Navegamos "pra cima" na arvore do HTML até encontrar o primeiro elemento com algum atributo único que contenha tudo da noticia
        Encontramos inicialmente o elemento de id "post-15371", serve? Não, claramente trata-se de um id peculiar DESTA url, queremos algo que esperamos ver em todas deste site
        Seguimos a navegação e batemos no elemento html de id "content", serve? Serve! IDs são únicos num .html, podemos esperar que esta id seja usada no main_wrapper em todas as noticias do site
        Assim, setamos, na classe de nosso scrapper, o parametro:
            main_wrapper_locator = (By.ID ,'content')

    Para este exemplo vamos extrair apenas o titulo 
    Agora vamos fazer o mesmo processo para achar o titulo:
        Clicamos com o botão direito sobre o titulo, e clicamos em "inspect" para ver o código fonte da página
        Vemos que a classe dele é class='entry-title' serve? Não! Clicamos Ctrl+F e pesquisamos por 'entry-title' para ver se ela aparece como classe em algum outro elemento dentro do main_wrapper
            Verificamos que,de fato, aparece. As noticias sugeridas logo abaixo do final da nossa noticia também utilizam essa classe.
        Continuamos navegando "pra cima" na arvore do HTML e encontramos "entry-header", serve? Sim! Pesquisando via Ctlr+F como fizemos antes, vemos que essa classe é única dentro de nosso main-wrapper
        Assim, setamos na classe de nosso scrapper, o parametro:
            title_locator = (By.CLASS_NAME ,'entry-header' )
        Porém veja, essa classe ainda não isola nosso titulo.. Entry-header é um elemento "pai" do nosso titulo, ele poderia conter outras coisas
        Então utilizaremos o title_locator_internal:
            Queremos encontrar algum selector que permita isolar o titulo DENTRO do que encontraremos com nosso title_locator
            Encontramos a classe 'entry-title', serve? Serve! Ela é a classe do nosso titulo dentro do title_locator que setamos
            Assim setamos o parametro:
                title_locator_internal = (By.CLASS_NAME ,'entry-header')

    Pronto! Com este simple processo nosso scrapper está pronto para extrair titulos do site https://atrombetanews.com.br/
    Basta repetir o mesmo processo com os outros parametros e em cerca de 20 minutos, o scrapper estará pronto.





'''

import os  # Allow use of shell commands
import sys
import abc
import time
import hashlib
import json
import unicodedata
import env
import logging

from datetime import datetime
from abc import ABC, abstractmethod
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import InvalidSessionIdException
from selenium.webdriver.chrome.options import Options

class UndesirableException(Exception):
    pass

class BaseScrapper(ABC):
    """
    Given the choice of which drive will be used,
    it is created and the arguments are configured.
    """
    textUndesirables = []
    undesirables = [] 
    dateEndingSeparator = "A_STRING" 

    def __init__(self, browser="chrome_headless"):
        self.set_selenium_driver(browser)

    def set_selenium_driver(self, browser="chrome_headless"):
        # Browser headless, for automatic executiond
        if browser == "chrome_headless":
            driver_dir = os.environ.get('CHROME')
            chrome_options = self.__set_chrome_options()
            self.driver = webdriver.Chrome(options=chrome_options,
                                           executable_path=driver_dir)
        # Browser for visual execution
        elif browser == "firefox":
            driver_dir = os.environ.get('FIREFOX')
            self.driver = webdriver.Firefox(executable_path=driver_dir)

    def __set_chrome_options(self):
        """
        Set arguments for headless chome.
        """
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=1920x1080")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--verbose')
        chrome_options.add_experimental_option("prefs", {
            "download.default_directory": "",
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing_for_trusted_sources_enabled": False,
            "safebrowsing.enabled": False
        })
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-software-rasterizer')

        return chrome_options

    def strip_accents(self,text):
        try:
            text = unicode(text, 'utf-8')
        except NameError: # unicode is a default on python 3 
            pass

        text = unicodedata.normalize('NFD', text)\
            .encode('ascii', 'ignore')\
            .decode("utf-8")
        return str(text)

    @property
    @classmethod
    @abstractmethod
    def main_wrapper_locator(cls):
        return NotImplementedError

    @property
    @classmethod
    @abstractmethod
    def scrapperSource(cls):
        return NotImplementedError    

    @property
    @classmethod
    @abstractmethod
    def text_locator(cls):
        return NotImplementedError 

    @property
    @classmethod
    @abstractmethod
    def subtitle_locator(cls):
        return NotImplementedError  

    @property
    @classmethod
    @abstractmethod
    def title_locator(cls):
        return NotImplementedError  

    @property
    @classmethod
    @abstractmethod
    def image_locator(cls):
        return NotImplementedError  

    @property
    @classmethod
    @abstractmethod
    def author_locator(cls):
        return NotImplementedError  

    @property
    @classmethod
    @abstractmethod
    def category_locator(cls):
        return NotImplementedError  

    @property
    @classmethod
    @abstractmethod
    def date_locator(cls):
        return NotImplementedError  

    @abstractmethod
    def title_locator_internal(cls):
        return NotImplementedError 

    @abstractmethod
    def subtitle_locator(cls):
        return NotImplementedError   
    
    @abstractmethod
    def image_locator(cls):
        return NotImplementedError  

    @abstractmethod
    def author_locator(cls):
        return NotImplementedError  

    @abstractmethod
    def author_locator_attribute(cls):
        return NotImplementedError  

    @abstractmethod
    def category_locator(cls):
        return NotImplementedError  

    @abstractmethod
    def video_locator(cls):
        return NotImplementedError  

    def access_article(self, articleUrl):
        self.driver.get(articleUrl)
        
    def get_main_wrapper(self, articleUrl):
        self.currentWrapper = self.driver.find_element(*self.main_wrapper_locator)

    def get_title(self):
        titleElement = self.driver.find_element(*self.title_locator)
        if(self.title_locator_internal != "NULL"):
            return self.treat_text(titleElement.find_element(*self.title_locator_internal).text)
        else:
            return self.treat_text(titleElement.text)

    def get_subtitle(self):
        if (self.subtitle_locator == "NULL"):
            return "NULL"
        else:
            try:
                return self.currentWrapper.find_element(*self.subtitle_locator).text
            except:
                return "NULL"
    
    def get_author(self): ##gold standard for non essentials
        if (self.author_locator == "NULL"):
            return "NULL"
        else:
            try:
                if(self.author_locator_internal == "NULL"):
                    authorElement =self.currentWrapper.find_element(*self.author_locator)
                else:
                    authorElement =self.currentWrapper.find_element(*self.author_locator).find_element(*self.author_locator_internal)

                if(self.author_locator_attribute == 'NULL'):
                    return self.treat_text(authorElement.text)
                else:
                    return self.treat_text(authorElement.get_attribute(self.author_locator_attribute))
            except Exception as e:
                print("Problemas no get_author: ", e)
                return "NULL"

    def treat_text(self, text):
        ret = text.replace('"', "'")
        ret = ret.replace("''", "'")
        ret = " ".join(ret.split())
        return ret

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
            if(self.dateStartSeparator != "NULL"): #Domingo, 19 de Abril de 2020, 12h:59 | Atualizado: vem do folhaMax
                dateText = self.dateTimeSeparator.join(dateText.split(self.dateStartSeparator)[1:])
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

    def get_category(self, articleUrl):
        categories = []
        if(self.category_locator != "NULL"):
            if(self.category_locator_internal == "NULL"):
                categoryElement =self.currentWrapper.find_element(*self.category_locator)
            else:
                categoryElement =self.currentWrapper.find_element(*self.category_locator).find_element(*self.category_locator_internal)
            try:
                categories.append(self.strip_accents( categoryElement.text.lower() ))
            except Exception as e:
                print(e)
                print("Problema temporario na captura de categoria NO ARTIGO, resolucao pendente")
                pass

        if(self.addUrlCategories):
            for lower in self.urlCategoryLowerBounds:
                if(lower in articleUrl):
                    urlCategories = articleUrl.split(lower)[1]
                    break
            for upper  in self.urlCategoryUpperBounds:
                if(upper in articleUrl):
                    urlCategories = urlCategories.split(upper)[0]
                    break
            urlCategories = urlCategories.split('/')
            categories.extend(urlCategories)

        if(self.addTagsCategories):
            tags = []
            tagsElement = self.currentWrapper.find_element(*self.tags_categories_locator)
            allTags = tagsElement.find_elements(*self.tags_categories_locator_internal)
            tags = [a.text.lower() for a in allTags if not any(und in a.text for und in self.tagsUndesirables)]
            categories.extend(tags)

        categories.extend(self.manualCategories)
        return list(set(categories))

    def get_main_image_url(self):
        if (self.image_locator == "NULL"):
            return "NULL"
        else:
            try:
                if (self.image_locator_internal == "NULL"):
                    imgElement = self.currentWrapper.find_element(*self.image_locator)
                else:
                    imgElement = self.currentWrapper.find_element(*self.image_locator).find_element(*self.image_locator_internal)
                return imgElement.get_attribute(self.image_locator_attribute)
            except Exception as e:
                print(e)
                return "NULL"


    def get_main_video_url(self):
        if (self.video_locator == "NULL"):
            return "NULL"

        else:
            try:
                if(self.video_locator_internal == "NULL"):
                    vidElement =self.currentWrapper.find_element(*self.video_locator)
                else:
                    vidElement =self.currentWrapper.find_element(*self.video_locator).find_element(*self.video_locator_internal)
                return vidElement.get_attribute(self.video_locator_attribute)
            except Exception as e:
                #print(e)
                return "NULL"


    def get_text(self):
        ret = ""
        trechos = self.currentWrapper.find_elements(*self.text_locator)
        for trecho in trechos:
            if(self.text_locator_internal != "NULL"):
                try:
                    paragraph =trecho.find_elements(*self.text_locator_internal)
                    # print(len(paragraph))
                    # for b in [ paragraph[-1] ]:
                    #     print("\n" + b.text)
                    # print(paragraph[-3].text)
                    # print("\n\n")
                    paragraph = [a.text for a in paragraph if not any(und in a.text for und in self.textUndesirables)]
                    #print(paragraph)
                    paragraph = " ".join(paragraph)
                    #print(paragraph)
                except:
                    continue
            else:
                if not any(und in trecho.text for und in self.textUndesirables):
                    paragraph = trecho.text
                else:
                    paragraph = ''

            if(len(paragraph) < 20): #Capaz de tratar muitos casos de coleta acidental de lixo
                continue
            ret+= paragraph
            ret+= " "
        if(len(ret) < 30):
            raise("Texto coletado pequeno demais, algo de errado aconteceu")
        return self.treat_text(ret)

    def scrap_article(self, articleUrl):
        for und in self.undesirables:
            if (und in articleUrl):
                raise UndesirableException("Artigos " + und + " estão na lista de indesejados e não serão coletados(não são noticias)")
        self.access_article(articleUrl)
        time.sleep(2)
        self.get_main_wrapper(articleUrl)
        features = dict()
        features['url'] = articleUrl
        features['source_name'] = self.scrapperSource
        features['title'] = self.get_title()
        features['subtitle'] = self.get_subtitle()
        features['publication_date'] = self.get_date()
        features['text_news'] = self.get_text()
        features['image_link'] = self.get_main_image_url()
        features['video_link'] = self.get_main_video_url()
        features['authors'] = self.get_author()
        features['categories'] = self.get_category(articleUrl)
        features['obtained_at'] = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        features['raw_file_name'] = self.html_file_name(articleUrl)
        self.save_html(features)
        print(features)
        return features

    def save_html(self, features):
        file_path = os.getenv('COLETORES') + "/" + self.scrapperSource + "/HTML/" + features['raw_file_name'] 
        with open(file_path, mode='w', encoding='utf-8') as f:
            f.write(self.driver.page_source)
        
    def scrap_urls_file(self, fileName, taskName):
        LOG_FILENAME = os.getenv('COLETORES') + "/" + self.scrapperSource + '/LOG/' + taskName + '.log'
        logging.basicConfig(filename=LOG_FILENAME, filemode ='w',level=logging.WARNING)
        count = 0
        latestTime = time.time()
        startTime = time.time()
        with open(fileName) as f:
            for url in f:
                print("Nova URL:", url)
                retry = 3
                while(retry > 0):
                    try:
                        urlDataPotentialPath = Path(os.getenv('COLETORES') + "/" + self.scrapperSource +"/HTML/" + hashlib.sha1(url.encode()).hexdigest()+ ".html")
                        if(urlDataPotentialPath.is_file()):
                            print("Skipping artigo #", count)
                            count = count + 1
                            break
                        data = self.scrap_article(url)
                        self.append_article_to_txt(data)
                        mark = time.time()
                        print ("Scrapping artigo #", count, "Unitary time:" ,mark - latestTime , 'Elapsed time:', mark - startTime)
                        count = count + 1
                        latestTime = mark
                        retry = 3
                        break
                    except UndesirableException as unde:
                        logging.warning(url + "\t" + str(type(unde)) + " : " + str(unde))
                        break
                    except InvalidSessionIdException as inval:
                        logging.exception(url)
                        #super(UOLScrapper, self).__init__()
                        self.set_selenium_driver()
                        break
                    except Exception as e:
                        print ("\t Retrying", retry, "times" , url)
                        retry = retry - 1
                        time.sleep(5)
                        if retry == 0:
                            logging.exception(url)

    def append_article_to_txt(self, features):
        file_path = os.getenv('COLETORES') +  "/" + self.scrapperSource + "/COLETA/" + features['source_name'].lower() + "_" + '_'.join(features['publication_date'].split('-')[0:2]) + ".txt"
        with open(file_path, mode='a', encoding='utf-8') as f:
            f.write(json.dumps(features, ensure_ascii=False) + '\n')
    
    def html_file_name(self,url):
        return hashlib.sha1(url.encode()).hexdigest()+ ".html"

    
    
