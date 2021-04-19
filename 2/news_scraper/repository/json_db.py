import json
import os


def insert_multiple_news(type, collected_data):
    """
    Receives news in json format and
    inserts it on json database file.
    """
    if type == 'news':
        database = 'NEWS_DB'
    elif type == 'checking':
        database = 'CHECKING_DB'
    else:
        raise 'Invalid type for select_urls on json database file'
    try:
        with open(os.environ.get(database)) as old_json:
            current_json = json.load(old_json)

        current_json.update(collected_data)
        with open(os.environ.get(database), mode='w') as f:
            f.write(json.dumps(current_json, indent=2))
    except Exception as e:
        print("Problem on passing news to json database")
        raise e


def select_urls():
    """
    Select all urls from a json database file.
    """
    try:
        with open(os.environ.get('URLS_DB')) as json_data:
            data = json.load(json_data)
        return data
    except Exception as e:
        print("Problem on selecting urls on url's json database file.")
        raise e
