import os

os.environ['PROJECT_DIR'] = os.path.dirname(os.path.abspath(__file__))

# ------------------------------------DRIVERS-----------------------------------
os.environ['CHROME'] = os.getenv('PROJECT_DIR') + '/drivers/chromedriver'
os.environ['FIREFOX'] = os.getenv('PROJECT_DIR') + '/drivers/geckodriver'
# --------------------------------------DATA-------------------------------------
os.environ['COLETORES'] = os.getenv('PROJECT_DIR') + '/COLETORES/IMPLEMENTADOS'
os.environ['CHECAGENS'] = os.getenv('COLETORES') + '/CHECAGENS/'
os.environ['NOTICIAS'] = os.getenv('COLETORES') + '/NOTICIAS'
