# Módulo 2

Esse módulo é responsável pela coleta dos seguintes sites:
* Aos Fatos
* Boatos
* Fato ou Fake
* Lupa

<br>
### Configurando os parâmetros:
Utilizando o arquivo news_scraper/env.py.example, crie o arquivo env.py no mesmo diretório.
Note que dentro deste arquivo há a Localização referente aos seguintes arquivos:
* Drivers do selenium;
* Pasta que armazena os dados coletados;
* Arquivo que contém as URL's a serem pesquisadas.


As localizações presentes são apenas uma sugestão de implementação e fazem uso das pastas **resources** e **database**. Essas localizações podem ser alteradas conforme a necessidade do projeto.
> É de suma importância que os drivers que serão selecionados sejão compatíveis com a versão dos browsers instalados nas máquinas que realizarão as coletas.

<br>
### Ambiente virtual geral:
Repare que as únicas dependências desse projeto são as bibliotecas Selenium e PyTesseract, logo é possível executar este projeto dentro de outros ambientes que atendam a essas dependências.
No entanto, é importante salientar que versões antigas do Selenium podem conflitar com certas versões de browsers, diante disso sugerimos que utilize as versões mais atualizadas tanto para o Selenium, quanto para os browsers.

<br>
### Ambiente virtual específico:
Caso queira é possível criar um **ambiente virtual apenas para esse módulo**, para isso deve ser atendido as seguintes dependências e passos:
**Dependências do sistema**:
* Python 3.8.2
* Venv (sudo apt install python3.8-venv)
* pip (sudo apt install python3-pip)

**Passos**:
1. Vá para a raiz do projeto.
2. Criando ambiente: `python3 -m venv ./venv`
3. Ativando ambiente:  `source venv/bin/activate`
4. Instalando dependências: `pip install -r requirements.txt`
5. Desativando ambiente: `deactivate`

<br>
### Executando o módulo:
Com o ambiente que contenha o Selenium, o PyTesseract e com todos os parâmetros configurados realizamos:
1. Movemos para a fonte do projeto :  `cd src`
2. Execute: `python3 run.py <arguments>`
	* Os _arguments_ irão definir qual o coletor será utilizado:
		* -aos_fatos		
		* -boatos
		* -fato-ou-fake
		* -lupa
3. As URL's do arquivo definido em env.py serão coletadas utilizando o coletor especificado em _arguments_ e serão salvos na pasta também definida no arquivo env.py.

<br>
### Arquitetura e estrutura de execução
O arquivo **run.py** é responsável por verificar qual o coletor será utilizado e chamar a controler para iniciar a execução.
O **controller/scrapers.py** irá gerenciar a execução, instanciando o coletor **crawler/custom_scraper.py** com uma de suas classes de implementação dependendo de qual site será coletado, suas implementações estão definidas em **crawler/custom/**.
As implementações dos coletores fazem uso da classe **crawler/base_crawler.py** que tem como única responsabilidade fornecer um driver do selenium para a coleta de dados.
A controller também é responsável por chamar o **repository/json_db.py** que tem duas funções:
* Fornecer as URL's provindas do arquivo definido em  **env.py** para a coleta.
Observe que há um exemplo do arquivo nesse projeto em database/urls_a_coletar.txt e que há um formato para essa leitura de URL's.
* Também é responsável por salvar os dados coletados em arquivos JSON. Repare que além dos dados específicos coletados, o html de cada página também é coletado, no entanto é salvo em uma pasta separada e com o nome do arquivo sendo uma hash de sua URL e esse nome é referenciado em um dos campos do JSON da coleta.

É importante ressaltar que ao realizar a coleta haverão problemas de captura de dados eventualmente, cada coletor irá salvar um arquivo JSON chamado **not_collected.json** com cada URL que não foi capaz de capturar seguido do erro ocasionado.
Esse arquivo deve ser revisado e apagado durante buscas de rotinas a longo prazo.
