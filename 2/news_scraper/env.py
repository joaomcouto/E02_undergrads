import os

os.environ['PROJECT_DIR'] = os.path.dirname(os.path.abspath(__file__))

# ------------------------------------DRIVERS-----------------------------------
os.environ['CHROME'] = os.getenv('PROJECT_DIR') + '/../resources/drivers/chromedriver'
os.environ['FIREFOX'] = os.getenv('PROJECT_DIR') + '/../resources/drivers/geckodriver'

# ------------------------------------DATABASE-----------------------------------
os.environ['DATABASE'] = os.getenv('PROJECT_DIR') + '/../database/'
os.environ['NEWS_DB'] = os.getenv('DATABASE') + 'news_database.json'
os.environ['CHECKING_DB'] = os.getenv('DATABASE') + 'checking_database.json'
os.environ['URLS_DB'] = os.getenv('DATABASE') + 'urls_database.json'

os.environ['DB_HOST'] = ""
os.environ['DB_NAME'] = ""
os.environ['DB_PORT'] = ""
os.environ['DB_USER'] = ""
os.environ['DB_PASS'] = ""
os.environ['DB_TABLE_X'] = ""


# --------------------------------------TEST-----------------------------------
os.environ['URLS'] = os.getenv('PROJECT_DIR') + '/../resources/url_examples/'
