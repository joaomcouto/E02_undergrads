import json
import os


def insert(url, type, source, collected_data, html=None, year=0, month=0):
    """
    Receives error or checking news in json format
    and inserts it on text-json database file.
    """
    source_folder = os.environ.get('DATABASE') + source + '/'
    if type == 'checking':
        html_folder = source_folder + 'HTML/'
        if month < 10:
            month = '0' + str(month)
        file_path = source_folder + f'COLETA/{source}_{year}_{month}.txt'
    elif type == 'error':
        file_path = source_folder + 'not_collected.json'
    else:
        raise 'DataBase error(Invalid type on json database file)'
    try:
        # SAVING HTMLs
        if type == 'checking':
            hash_value = collected_data['raw_file_name']
            with open(f'{html_folder}{hash_value}.html', "w") as file:
                file.write(html)
        # SAVING COLLECTED DATA
        with open(file_path, mode='a', encoding='utf-8') as f:
            f.write(json.dumps(collected_data, ensure_ascii=False) + '\n')
    except Exception as e:
        print(e)
        print("Problem while saving data")
        raise e


def select_urls(source):
    """
    Select all urls from a json database file.
    """
    try:
        file_path = os.environ.get('URLS_DB') + 'urls_' + source + '.txt'
        with open(file_path) as json_data:
            data = json.load(json_data)
        return data
    except Exception as e:
        print("Problem on selecting urls on url's json database file.")
        raise e
