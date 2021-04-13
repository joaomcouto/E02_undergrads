# News_Scraper
## Execution:
### Initial requirements:
* Pytho 3.8.2
* Venv (sudo apt install python3.8-venv)
* pip (sudo apt install python3-pip)

### Initial setup:
1. Create enviroment:    `python3 -m venv ./venv`
2. Activate enviroment:  `source venv/bin/activate`
3. Install requirements: `pip install -r requirements.txt`

### Execute:
1. Activate enviroment:  `cd news_scraper && source venv/bin/activate`
2. Execute: `python3 run.py <arguments> <url>`
	* Arguments:
		* -I : execute firefox driver with visual execution
		* -init: execute initial commands for enviroment
	* URL: news url to be scraped.
3. Exit: `deactivate`
