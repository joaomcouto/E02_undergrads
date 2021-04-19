# News_Scraper
### Initial requirements:
* Pytho 3.8.2
* Venv (sudo apt install python3.8-venv)
* pip (sudo apt install python3-pip)

### Initial setup:
1. Create enviroment:    `python3 -m venv ./venv`
2. Activate enviroment:  `source venv/bin/activate`
3. Install requirements: `pip install -r requirements.txt`

### Execution:
1. Activate enviroment:  `source venv/bin/activate && cd news_scraper`
2. Execute: `python3 run.py <arguments>`
	* Arguments:
		* -I <URL>: execute firefox driver with visual execution and print data.
		* -init: execute initial commands for enviroment (only execute once).
		* -r: execute URL's on database for routine execution.
3. Exit: `deactivate`
