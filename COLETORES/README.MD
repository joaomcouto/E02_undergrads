## DESCRIPTION:
## 1 Coletores
- Com o objetivo de permitir a criação em larga escala de coletores, foi desenvolvido o módulo base_scrapper que define a classe base "BaseScrapper" a ser utilizada em todos coletores desenvolvidos para a coleta de notícias e/ou fact-checking neste projeto

- Esta classe semi-abstrata define uma série de métodos "padrão" que buscam ser robustos o suficiente para conseguir coletar os principais dados de interesse de quaisquer sites de notícia ou verificação de fatos

- O objetivo é permitir que um coletor customizado para um site inédito possa ser desenvolvido em poucas linhas de código, bastando definir os parametros para o funcionamento deste BaseScrapper e, ocasionalmente, implementando/redefinindo métodos (na subclasse) no raro caso em que alguma das lógicas de coleta presentes no baseScrapper não atende às especificidades de algum portal de notícias/fact-checking

- Assim, na eventualidade da lógica de um método padrão não conseguir lidar com as características do código fonte de uma página no contexto da coleta de algum dado de interesse do site (i.e título, autor), deve-se implementar e redefinir o respectivo método de coleta desse dado na subclasse que herda baseScrapper. Aqui, vale ressaltar que em várias ocasiões os métodos "padrão" servem como base para a criação de métodos customizados nestes casos, e que, na maioria dos casos, basta trocar uma ou duas linhas sobre como eles funcionam

## 1.1 Parâmetros de entrada (Coletores)

### 1.1.1 NOÇÕES BÁSICAS: a hierarquia de locators e o parametro attribute (IMPORTANTE!!!)
- Para possibilitar o entedimento do parametros de uso dos métodos deste módulo é necessário entender uma noção básica comum entre todos eles: a hierarquia de locators

- A hierarquia de locators constitui a definição de 3 instâncias do mecanismo "By" do framework Selenium. Em todos os métodos neste módulo, a ativação sequencial dessas 3 instâncias deve possibilitar ao BaseScrapper encontrar e isolar o elemento de interesse em cada método. 

- A primeira dessas 3 instâncias, main_wrapper_locator, é compartilhada entre todos os métodos e representa um localizador para o elemento HTML (único no código fonte) que contém como nodes filhos todos os elementos HTML com as informações que se espera coletar.

- As duas últimas instâncias, x_locator e x_locator_internal , específicas de cada método x, representam uma combinação de localizadores que quando executados sequencialmente dentro do elemento HTML encontrado pelo main_wrapper_locator especificado acima, devem encontrar, isoladamente, o(s) elemento(s) de interesse do método x.

- Assim, por exemplo,  para o método get_title, definimos em nossa subclasse os parametros title_locator e title_locator_internal, e então, ao ser chamado, o método get_title vai, (1) buscar por title_locator dentro do retorno de main_wrapper_locator e (2) buscar por title_locator_internal dentro do resultado de 1.

- Assim conclui-se que para encontrar um dado de interesse não é necessário que o localizador para ele seja único no código fonte da página inteira e sim que a combinação dos três localizadores, executados sequencialmente, um dentro do outro, seja capaz de isolar APENAS o dado que buscamos com o método. 

- Observa-se que às vezes não precisamos do locator x_locator_internal, a combinação do main_wrapper_locator com x_locator muitas vezes é suficiente para isolar o elemento de interesse. Neste caso, definimos x_locator_internal = "NULL" , os métodos de baseScrapper utilizarão apenas os dois primeiros.

- Por fim, outra noção básica comum entre vários métodos é a definição do parametro x_locator_attribute. Se este for diferente de "NULL", os métodos retornam o atributo x_locator_attribute dos elementos HTML encontrados pela hierarquia de locators definida acima ao invés do atributo texto (.text) deles.





- Em resumo:
	-  A ideia básica de uso dos métodos aqui presentes é a definição de 3 níveis de finders do Selenium, 1 compartilhado por todos os métodos e 2 especificos de cada método
	  	- `main_wrapper_locator, finder para o elemento HTML UNICO NA PAGINA que contém todas a informações que se deseja coletar com o Scrapper.`
  		- `x_locator, IDEALMENTE o finder para os elementos HTML dentro do main_wrapper que contenham APENAS o dado que um certo método busca coletar, se x_locator não for o suficiente para isolar apenas os elementos que o método busca coletar, utilizamos o x_locator_internal`
  		- `x_locator_internal, deve então conter o finder para os elementos HTML dentro de x_locator que contenham APENAS o dado que um dado método busca coletar`

	- Com esses parametros/finders definidos, os métodos então buscam dentro de main_wrapper o elemento x_locator e, se o x_locator_internal for diferente de "NULL", buscam por x_locator_internal dentro do elemento que foi encontrado por x_locator

	- Observamos que a probabilidade de que estes dois níveis de filtro sejam insuficientes, considerando todas as formas que temos de encontrar elementos no selenium, é pragmaticamente nula

	- Uma vez isolados os elementos duas coisas podem acontecer:
    		1 - O método vai extrair o texto .text dos elementos isolados
    		2 - Podemos definir o parametro x_locator_attribute, neste caso, o método vai extrair o valor do atributo x_locator_attribute dos elementos HTML isolados
    
    
    
    
    
    

## 1.1.2 Coletores: métodos e parametros

A seguir, explicitamos os métodos do modulo base_scrapper juntamente com os parametros que devem ser definidos para que um coletor baseado nessa arquitetura proposta possa funcionar. Inicialmente, descreveremos os métodos que seguem uma lógica compartilhada simples e posteriormente aqueles mais complexos feitos "sob medida" 

---
### html_file_name(self,url):
- Parametros de chamada:
	- `url: link para uma notícia/checagem`
		
Retorna o nome do arquivo contendo o código fonte da url recebida como parametro da função. O nome do arquivo é calculado como o sha1 (via hashlib) da url apendado da extensão ".html"


---
### append_article_to_txt(self, features):
- Parametros de chamada:
	- `features: objeto JSON retornado por uma chamada à função scrap_article`
		
Salva no .txt correto a coleta de um artigo (presente em features) feita através da função scrap_article. Para tal extrai de features['publication_date'] o ano/mes da publicação e de features['source_name'] sua fonte. Então apenda os dados ao arquivo .txt referente ao ano,mes e fonte do artigo.
Assim, uma notícia publicada em Abril de 2021 no G1, terá sua coleta salva no arquivo G1/COLETA/G1_2021_04.txt
   
---
### scrap_urls_file(self, fileName, taskName):**
- Parametros de chamada:
	- `fileName: arquivo .txt contendo em cada linha, uma URL a ser coletada`
		
	- `taskName: string contendo um nome para a tarefa de coleta sendo realizada. Este nome é utilizado para criar o arquivo de logging.`
		
Efetiva, via scrap_article(), a coleta de multiplos artigos de uma mesma fonte de notícias/checagem

---
### save_html(self, features):**
- Parametros de chamada:
	- `features: objeto JSON retornado por uma chamada à função scrap_article`
		
Salva, na pasta correta, o código fonte (.html) de um artigo coletado via scrap_article(). Para tal, extrai de features['source_name'] sua fonte e calcula o nome do arquivo html através da função html_file_name()
Assim, uma notícia publicada no G1, terá seu código fonte salvo na pasta G1/HTML/ com o nome html_file_name(url_da_noticia)

---
### scrap_article(self, articleUrl):**
- Parametros de chamada:
	- `articleUrl: link para uma notícia/checagem`
		
- Parametros definidos via atributos de subclasse:
	- `undesirables: uma lista de strings na qual cada string é uma substring de URL tal que se articleURL conter alguma delas, uma exceção do tipo UndesirableException é lançada`
		
Efetiva a coleta do artigo em articleUrl via chamadas a todas as funções get_x() a menos que a URL contenha alguma substring. Retorna um objeto JSON com as 'features' do artigo (url, fonte, título, subtitulo, data de publicação, texto do artigo, link para imagem principal, link para video principal, autores, cateogiras, data de coleta, nome do arquivo HTML contendo o código fonte da página)

---
### get_text(self):**

- Parametros definidos via atributos de subclasse:
	- `text_locator: conforme descrito em 1.1.1`
		
	- `text_locator_internal: conforme descrito em 1.1.1`
		
	- `textUndesirables: lista de strings`

	Função de comportamento padrão conforme descrito em 1.1.1 Retorna uma string com o texto do artigo, eliminando paragrafos que contenham alguma das substrings listada em textUndesirables (isso permite a eliminação por exemplo, de propagandas anexas no corpo do texto de artigos que são indistinguíveis de um parágrafo qualquer do texto, tal como 'clique aqui para visitar nosso canal no youtube')


---
### get_main_video_url(self):**

- Parametros definidos via atributos de subclasse:
	- `video_locator`	
	- `video_locator_internal `
	- `video_locator_attribute`
		
Função de comportamento padrão conforme descrito em 1.1.1. Retorna a URL do vídeo principal 'no topo' de um artigo caso esteja presente (do contrário retorna a string "NULL")

---
### get_main_image_url(self):**

- Parametros definidos via atributos de subclasse:
	- `image_locator`
	- `image_locator_internal`
	- `image_locator_attribute`
	
Função de comportamento padrão conforme descrito em 1.1.1. Retorna a URL da imagem principal 'no topo' de um artigo caso esteja presente (do contrário retorna a string "NULL")

---
### get_category(self, articleUrl):**
- Parametros de chamada:

	- `articleUrl: link para um artigo`

- Parametros definidos via atributos de subclasse:
 
    - `category_locator:`
		
    - `category_locator_internal :`
		
    - `addUrlCategories: booleano, define se a função deverá buscar por categorias na URL da notícia`
		
    - `urlCategoryLowerBounds: subtring de articleUrl que delimita o início da seção da URL contendo a categoria de interesse (i.e em g1.globo.com/bemestar/coronavirus/noticia/2020/09/15/oms.. deve ser '.com/')` 
		
    - `urlCategoryUpperBounds: subtring de articleUrl que delimita o início da seção da URL contendo a categoria de interesse (i.e em g1.globo.com/bemestar/coronavirus/noticia/2020/09/15/oms.. deve ser '/noticia')`

    - `addTagsCategories: booleano, define se a função deverá buscar por categorias em tags presentes na página da noticia`

    - `tags_categories_locator: locator para o elementos com as tags`
		
    - `tags_categories_locator_internal: locator para as tags dentro de`
		
    - `tagsUndesirables`
    
		
Existem três possíveis fonte de extrair categorias de um artigo: um elemento categoria explicito na página do artigo, um coletania de tags (i.e bolsonaro, política, vacina, CPI) ou ainda a própria URL da noticia (tal como 'saúde' em noticias.uol.com.br/saude/...html)
Essa função permite que todas as três sejam coletadas.

---
### get_date(self):**

- Parametros definidos via atributos de subclasse:
	- `date_locator `
		
	- `date_locator_internal`
			
	- `dateHasTime, booleano, define se a data presente nos artigos do portal têm a hora da publicaçao ou não (usada tanto para artigos que têm um atributo dateTime quanto para artigos que não)`
		
	- `dateHasDateTimeAttribute, booleano, define se o elemento HTML com a data de publicação tem um atributo com no formato datetime (é o caso para  a grande maioria dos sites)`
		
	- `dateTimeAttribute, se o booleano acima for True, define qual o nome do atributo padrão datetime, na grande maioria (mas não todos) os sites, o atributo é apenas 'datetime'  `
	
	- Os parametros a seguir servem para o caso em que um determinado site não oferece um atributo na formatação datetime no elemento HTML associado com a data de publicação do artigo. Para facilitar o entendimento, eles utilizarão a string "Domingo, 19 de Abril de 2020, 12h:59 | Atualizado:" como exemplo corrente de .text retornado pelos locators de data definidos acima
		
		- `dateStartSeparator, define qual substring do .text encontrado faz fronteira com o inicio da a string com a data, no exemplo, seria ", " pois assim conseguimos separar a data da substring "Domingo, "`
			
		- `dateEndingSeparator, define qual substring do .text encontrado faz fronteira com fim da string com a data, no exemplo, seria " |", pois assim conseguimos separar a data da substring " | Atualizado"`
			
		- `dateTimeSeparator, define qual a substring a ser utilizada para separar a data do horário de publicação, no exemplo seria ", " pois assim conseguimos seprar a substring data "19 de Abril de 2020" da substring horario "12h:59"`
			
		- `hourMinuteSeparator, define qual a subtring que separar o minuto da hora de publicação, no exemplo, "h:" `
			
		- `dayMonthYearSeparator, define qual a substring que separar o dia, mes,ano de publicação, no exemplo " de "`
			
		- `monthNeedsMapper, deve ser True se o mês presente no elemento de dada do artigo for escrito de alguma forma que não o número do mês(por exemplo abril ao invés de 04 ou 4). É o caso do exemplo corrente.`
			
		- `dateMonthMapper, deve ser um dicionario capaz de traduzir um mês escrito por extenso no formato do site para um número de 1 a 12, no exemplo seria dateMonthMapper = {
        'Janeiro': 1,
        'Fevereiro': 2,
        'Março': 3,
        'Abril': 4,
        'Maio': 5,
        'Junho': 6,
        'Julho': 7,
        'Agosto': 8,
        'Setembro': 9,
        'Outubro': 10,
        'Novembro': 11,
        'Dezembro': 12
    } `
			
		- `yearNeedsMapper, deve ser True se o ano presente no elemento de data do artigo for de alguma forma que não o ano completo (como por exemplo numa data na formatação 01/11/20 ao invés de 01/11/2020) `
			
		- `dateYearMapper, deve ser um dicinario capaz de traduzir a formatação de ano presente no site para o ano completo (como por exemplo numa data na formatação 01/11/20 ao invés de 01/11/2020. Neste caso o mapper devera ter uma entrada '20':2020) `

Essa função permite a extração da data de publicação de artigos. Existem duas maneiras para isso acontecer: via um atributo datetime do elemento HTML da data ou apartir do texto (node .text) visivel em tela ao acessar a URL do artigo. Ao final, retorna uma string 'Ano-mes-dia hora:minuto:segundo'
---
### get_author(self):

- Parametros definidos via atributos de subclasse:
	- `author_locator`
	- `author_locator_internal`
	- `author_locator_attribute`

---
### treat_text(self, text):
- Parametros de chamada:
	- `text: string `
Efetiva a troca de aspas duplas por aspas simples
---
### get_subtitle(self):

-Parametros definidos via atributos de subclasse:
	- `subtitle_locator `
	
---
### get_title(self):**

- Parametros definidos via atributos de subclasse:
	- `title_locator `
		
	- `title_locator_internal`
---
### get_main_wrapper(self, articleUrl):
- Parametros de chamada:
	- `articleUrl`
	
- Parametros definidos via atributos de subclasse:
	- `main_wrapper_locator: deve ser um localizador By do selenium que permita isolar no código fonte da página o wrapper principal do artigo que contenha em seus nodes filhos todas as informações que se espera coletar com este scrapper`

Modifica o atributo de instancia "currentWrapper" fazendo com que armazene o elemento HTML associado com o wrapper global do artigo
	
---
### access_article(self, articleUrl):
- Parametros de chamada:
	- `articleUrl`
	
---
### strip_accents(self,text):
- Parametros de chamada:
	- `text: string`
Efetiva
	
---
### __set_chrome_options(self):

---
### set_selenium_driver(self, browser="chrome_headless"):
- Parametros de chamada:
	- `browser: firefox ou chrome_headless`
Inicializa o driver do selenium sobre o qual os métodos do scraper operam. Se o parametro browser for firefox, o scraper oferece um interface em tempo real que permite a visualização da página atualmente sendo acessada. Do contrário, utiliza o chromedriver para efetivar as operacões em background, sem interface.

# Definindo um novo scrapper

### EXEMPLO PRATICO SIMPLES: 

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
    
### EXEMPLO PRÁTICO MEDIO: 

preparando um scrapper para extrair o titulo do site https://atrombetanews.com.br/ (USO DE X_LOCATOR + X_LOCATOR_INTERNAL + .TEXT (sem x_locator_attribute))

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
