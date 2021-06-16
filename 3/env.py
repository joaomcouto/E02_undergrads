import os



os.environ['PROJECT_DIR'] = os.path.dirname(os.path.abspath(__file__))

os.environ['CHROME'] = os.getenv('PROJECT_DIR') + '/resources/drivers/chromedriver_3'
os.environ['FIREFOX'] = os.getenv('PROJECT_DIR') + '/resources/drivers/geckodriver_3'
os.environ['COLLECTED_DIR'] = os.getenv('PROJECT_DIR') + '/collected_data/'

os.environ['DATA_DIR'] = "/scratch4/E02_Undergrads/data_dump"
