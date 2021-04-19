from selenium.webdriver.common.by import By

URL_MAP = {
    'G1': {
        'type': 'news',
        'url_fragment': ('g1.globo.com', 'g1.globo.com/fato-ou-fake/'),
        'has_custom_crawler': False,
        'fact_checking': False,
        'has_js': None
    },
    'UOL': {
        'type': 'news',
        'url_fragment': ('uol.com.br', 'piaui.folha.uol.com.br/lupa'),
        'has_custom_crawler': False,
        'fact_checking': False,
        'has_js': None
    },
    'BBC': {
        'type': 'news',
        'url_fragment': 'www.bbc.com',
        'has_custom_crawler': False,
        'fact_checking': False,
        'has_js': None
    },
    'Aos Fatos': {
        'type': 'fact_checking',
        'url_fragment': 'aosfatos.org',
        'has_custom_crawler': False,
        'has_js': False,
        'elements': {
            'title': [
                ('single_element', By.XPATH, '/html/body/main/section/article/h1'),
                ('get_text', None, None)],
            'date': [
                ('single_element', By.CLASS_NAME, 'publish_date'),
                ('get_text', None, None)],
            'authors': [],
            'category': [],
            'text': [
                ('multi_elements', By.XPATH, '/article/p'),
                ('get_text', None)],
            'main_img': [
                ('verify_existence', )],
            'main_video': [],
            'veredict': [
                (By.XPATH, '/html/body/header/nav[1]/ul/li[1]/div/div/ul/li[7]/a'),
                ('get_text', None)]
        }
    },
    'Lupa': {
        'type': 'fact_checking',
        'url_fragment': 'piaui.folha.uol.com.br/lupa',
        'has_custom_crawler': False,
        'has_js': None
    },
    'Boatos': {
        'type': 'fact_checking',
        'url_fragment': 'boatos.org',
        'has_custom_crawler': False,
        'category': '',
        'fact_checking': ''
    },
    'Comprova': {
        'type': 'fact_checking',
        'url_fragment': 'projetocomprova.com.br',
        'has_custom_crawler': False,
        'has_js': None
    },
    'Fato-ou-Fake': {
        'type': 'fact_checking',
        'url_fragment': 'g1.globo.com/fato-ou-fake/',
        'has_custom_crawler': False,
        'has_js': None
    },
    'e-farsas': {
        'type': 'fact_checking',
        'url_fragment': 'e-farsas.com',
        'has_custom_crawler': False,
        'has_js': None
    }
}


def get_source_information(url):
    """
    Receives a url and returns its source and information
    """
    for key, value in URL_MAP.items():
        # Check for urls with common passages
        if len(value['url_fragment']) == 2:
            if value['url_fragment'][1] not in url and value['url_fragment'][0] in url:
                return key, URL_MAP[key]
        # Check for url with unique passages
        elif value['url_fragment'] in url:
            return key, URL_MAP[key]
    raise 'Source not found for URL'
