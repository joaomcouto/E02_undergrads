import json
import os


def insert_multiple_news(formated_news):
    """
    Receives news in json format and
    inserts it on json database file.
    """
    try:
        with open(os.environ.get('JSON_DB')) as old_json:
            current_json = json.load(old_json)

        current_json.update(formated_news)
        with open(os.environ.get('JSON_DB'), mode='w') as f:
            f.write(json.dumps(current_json, indent=2))
    except Exception as e:
        print("Problem on passing news to json database")
        raise e
