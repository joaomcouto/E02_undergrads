# E02
Arcabouço computacional para detecção de notícias falsas.


### Base de dados:
A base de dados corresponde aos arquivos:
* DATASET_MPMG-FakeNews_matched.txt
* DATASET_MPMG-TrueNews_selected.txt

Para a leitura da base de dados há um arquivo na pasta utils chamado _leitura_dataset.py_ com uma função exemplo que lê toda a base e imprime as três primeiras notícias de cada parte. O código pode ser executado a partir do seguinte comando:

```
python3 leitura_dataset.py
```
<br>

### Configurando o sitema:
* **Versão dos drivers do selenium**:
	É de suma importância que os drivers que serão selecionados sejão compatíveis com a versão dos browsers instalados nas máquinas que realizarão as coletas. Os drivers se encontram na pasta _/drivers_ e podem ser atualaizados nos seguintes links:
	* [chromedriver](https://chromedriver.chromium.org/downloads)
	* [geckodriver](https://github.com/mozilla/geckodriver/releases)
* **Variáveis de ambiente**
	Existem variáveis de ambiente que são utilizadas pelo sistema e estão localizadas no arquivo _/env.py_. Essas variáveis estão preenchidas para funcionar sem modificações iniciais, porém caso haja a necessidade de movimentar arquivos pelo código é importante se atentar a esses parâmetros.
	Um exemplo é a localização dos drivers que é definida nesse arquivo.

<br>

### Dependências e ambiente:
* **Mínimo para execução**:

	* **Dependências do sistema**:
		* Python 3.8.2
		* PIP 3 (sudo apt install python3-pip)

	* **Instalando dependências:**
		`pip3 install -r requirements.txt`
<br>

* **Ambiente Geral**:
	Repare que as únicas dependências desse projeto são as bibliotecas Selenium e PyTesseract, logo é possível executar este projeto dentro de outros ambientes que atendam a essas dependências.
	No entanto, é importante salientar que versões antigas do Selenium podem conflitar com certas versões de browsers, diante disso sugerimos que utilize as versões mais atualizadas tanto para o Selenium, quanto para os browsers.
<br>

* **Ambiente virtual específico**:
	Caso queira é possível criar um **ambiente virtual apenas para esse módulo**, para isso deve ser seguido os seguintes passos utilizando o **Venv** (sudo apt install python3.8-venv):
	1. Vá para a raiz do projeto.
	2. Criando ambiente: `python3 -m venv ./venv`
	3. Ativando ambiente:  `source venv/bin/activate`
	4. Instalando dependências: `pip install -r requirements.txt`
	5. Desativando ambiente: `deactivate`

<br>

### Executando:
Com o ambiente que contenha o Selenium, o PyTesseract e com todos os parâmetros configurados executamos o seguinte código na raiz do projeto:
`python3 main.py <parâmetros>`

Onde os parâmtros dividem qual o tipo de busca será feita com qual fonte. A divisão do tipo se dá entre busca por URLs ou coletores que buscam todos os dados de um site.

* **Parâmetros para busca de Urls:**
 `-url <fonte>`

	Possíveis fontes:
	* -all
	* AOSFATOS
	* BOATOS
	* COMPROVA
	* ESTADAOVERIFICA
	* FATOOUFAKE
	* LUPA

	Repare que pode ser passado o parâmtro -all para a busca de URL, assim reallizando a busca simultânea de todas as fontes. Então, por exemplo, os comandos:
	```
	python3 main.py -url LUPA
	```
	ou
	```
	python3 main.py -url -all
	```
<br>
<br>

* **Parâmetros para busca de coletores:**
 `-coletor <fonte> <url>`

	A URL deve ser uma notícia ou checagem pertencente à fonte. As fontes  dos coletores estão dispostas no final do arquivo. Tanto as notícias como as checagens se encaixam nessa categoria e não há diferenciação na chamada.
	Então, por exemplo, teremos as seguintes chamadas de execução:

	```
	python3 main.py -coletor ADVENTISTAS http://www.adventistas.com/2020/04/02/novo-coronavirus-tem-algo-errado-com-esse-virus-da-covid19/
	```

	ou

	```
	python3 main.py -coletor AOSFATOS https://www.aosfatos.org/noticias/nao-e-verdade-que-estados-recebem-r-19-mil-por-cada-morte-de-covid-19/
	```

	**Fonte de coletores:**
	* Notícias:
		* ADVENTISTAS
		* ALIADOSBRASIL
		* ATROMBETA
		* BBC
		* CARTAPIAUI
		* CONEXAOAMAZONAS
		* CRITICANACIONAL
		* DIARIODOPODER
		* ESTIBORDO
		* ESTUDOSNACIONAIS
		* FOLHADAPOLITICA
		* FOLHADAREPUBLICA
		* FOLHAMAX
		* G1
		* GAZETABRASIL
		* JORNAL21BRASIL
		* JORNALDACIDADE
		* LUISCARDOSO
		* OGRITOCENSURADO
		* OLHOABERTOPR
		* QUESTIONESE
		* REVISTAAMAZONIA
		* REVISTAOESTE
		* RSAGORA
		* TERCALIVRE
		* TERRABRASIL
		* TIERRAPURA
		* TRIBUNANACIONAL
		* UOL
	* Checagens:
		* AOSFATOS
		* BOATOS
		* COMPROVA
		* ESTADAOVERIFICA
		* FATOOUFAKE
		* LUPA


### Dados coletados:
Os dados são divididos da mesma forma que o sistema, há um formato para a busca de URLs e um formato para os coletores de sites.
* **Busca de URLs:**
	O arquivo contendo as URLs coletadas é salvo na pasta BUSCA_URLS/URLS. Os arquivos são organizados pelo nome da agência  da seguinte maneira: urls_nome_da_agencia.txt. Internamente os arquivos são organizados em jsons contendo url, fonte da url, tipo (notícia ou checagem) e a data de obtenção. O módulo está disponível para a coleta de urls de todas as seis agências de checagens utilizadas.

* **Coletores de sites:**
	A pasta de cada coletor, notícia ou checagem é disposta da seguinte forma:
	```python
		../NOMEDOVEICULO
			|_HTML/
			|_COLETA/
			|_LOG/
			|_código do coletor
	```

	Na pasta /HTML ficam salvos os códigos-fontes das páginas coletadas, na pasta /LOG ficam salvos possíveis erros de coleta e a pasta /COLETA guarda os arquivos contendo as coletas. Os arquivos em COLETA são organizados por mês e ano da publicação da notícia, sendo nomeados: nomeveiculo_ano_mes.txt. Internamente esses arquivos são organizados em um json por linha contendo as informações coletadas como título, data de publicação, autor, texto da notícia, etc.

<br>

### Documentação completa do código e seus processos
* **Coletores**:
	Na pasta /COLETORES é possível encontrar um README explicando e documentando com mais detalhes todo o funcionamento dos coletores de dados de noticias que foram desenvolvido com base no BaseScraper, o módulo criado para possibilitar o desenvolvimento da grande quantidade de coletores feitos para essa parte do projeto.<br>
	
	[Arquivo com explicação/documentação dos Coletores](COLETORES/README.MD)<br>
	
	Os coletores de checagens são independentes dos coletores de notícias, onde o COMPROVA e ESTADAOVERIFICA são scripts independentes, enquanto os outros coletores de checagens fazem uso dos aquivos base_crawler e custom_scraper.
	
* **Busca URLS**:
	As buscas são realizadas por scripts independentes presentes dentro da pasta.
