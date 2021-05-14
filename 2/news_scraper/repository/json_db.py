import json
import os


def insert(type, source, collected_data, year=0, month=0, url_htmls={}):
    """
    Receives news in json format and
    inserts it on json database file.
    """
    source_folder = os.environ.get('DATABASE') + source + '/'
    if type == 'checking':
        html_folder = source_folder + 'HTML/'
        file_path = source_folder + str(year) + f'/{source}-{year}-{month}.json'
    elif type == 'error':
        file_path = source_folder + 'not_collected.json'
    else:
        raise 'DataBase error(Invalid type on json database file)'
    try:
        # Verify if file doesn't exist
        if not os.path.exists(file_path):
            with open(file_path, 'w', encoding='utf-8') as outfile:
                json.dump({}, outfile)
            current_json = {}
        # Load file data if already exists
        else:
            with open(file_path) as old_json:
                current_json = json.load(old_json)
            print(collected_data)
        # Saving the new data
        current_json.update(collected_data)
        print(current_json)
        with open(file_path, mode='w', encoding='utf-8') as f:
            f.write(json.dumps(current_json, indent=2, ensure_ascii=False))
    except Exception as e:
        print(e)
        print("Problem on passing data to json database")
        raise e

    # SAVING HTMLs
    if type == 'checking':
        try:
            index_file = source_folder + 'html_url_indexes.json'
            # Create file if doesn't exist
            if not os.path.exists(index_file):
                with open(index_file, 'w', encoding='utf-8') as outfile:
                    json.dump({}, outfile)
                indexes = {}
                file_number = 0
            # Load file data if already exists
            else:
                with open(index_file) as old_json:
                    indexes = json.load(old_json)
                if len(indexes) == 0:
                    file_number = 0
                else:
                    last_file_url = max(indexes, key=indexes.get)
                    file_number = indexes[last_file_url]

            for url, html in url_htmls.items():
                file_number += 1
                # Add url index
                indexes.update({url: file_number})
                # Create html file
                with open(f'{html_folder}{file_number}.html', "w") as file:
                    file.write(html)

            # Append new html files indexes
            with open(index_file, mode='w', encoding='utf-8') as f:
                f.write(json.dumps(indexes, indent=2, ensure_ascii=False))
        except Exception as e:
            print("Problem on saving HTML files")
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
