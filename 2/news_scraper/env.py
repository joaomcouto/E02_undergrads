import os

os.environ['PROJECT_DIR'] = os.path.dirname(os.path.abspath(__file__))

os.environ['CHROME'] = os.getenv('PROJECT_DIR') + '/../resources/drivers/chromedriver'
os.environ['FIREFOX'] = os.getenv('PROJECT_DIR') + '/../resources/drivers/geckodriver'
os.environ['COLLECTED_DIR'] = os.getenv('PROJECT_DIR') + '/../collected_data/'
