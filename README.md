# Sistema de coleta


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

**Parâmetros para busca de Urls:**
 `-url <fonte>`

Possíveis fontes:
* -all
* ESTADAOVERIFICA
* BOATOS
* COMPROVA
* AOSFATOS
* LUPA
* FATOOUFAKE

Repare que pode ser passado o parâmtro -all para a busca de URL, assim reallizando a busca simultânea de todas as fontes. Então, por exemplo, os comandos:
`python3 main.py -url LUPA`
ou
`python3 main.py -url -all`

<br>

**Parâmetros para busca de coletores:**
 `-coletor <fonte> <url>`

A URL deve ser uma notícia ou checagem pertencente à fonte. As fontes  dos coletores estão dispostas no final do arquivo. Tanto as notícias como as checagens se encaixam nessa categoria e não há diferenciação na chamada.
Então, por exemplo, teremos as seguintes chamadas de execução:

```python
python3 main.py -coletor ADVENTISTAS http://www.adventistas.com/2020/04/02/novo-coronavirus-tem-algo-errado-com-esse-virus-da-covid19/
```

ou

```python
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
