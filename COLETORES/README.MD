## DESCRIPTION:
Este modulo define a classe base "BaseScrapper" a ser utilizada em todos scrappers desenvolvidos para a coleta de noticias e/ou fact-checking neste projeto

Esta classe semi-abstrata define uma serie de métodos "padrão" que buscam ser robustos o suficiente para conseguir coletar dados de quaisquer sites de noticia ou verificação de fatos

O objetivo é permitir que um scrapper para um site inédito possa ser desenvolvido em poucas linhas de código, bastando definir os parametros deste BaseScrapper

Na eventualidade da lógica de um método dessa classe não se encaixar com a coleta de um campo de um dado site, basta redefinir o método na classe scrapper que o herda.
    Observamos que os métodos definidos aqui servem de base para a criação de métodos customizados nestes casos, e que, na maioria dos casos, basta trocar uma ou duas linhas sobre como eles funcionam


## NOÇÕES BÁSICAS

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
