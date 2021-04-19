# Outline:
def get_database_json_format(source, data):
    formatted_data = {
        data['original_url']: {
            'source': source,
            'title': data['title'],
            'date': data['date'],
            'img': data['img'],
            'keywords': data['keywords'],
            'summary': data['summary'],
            'text': data['text'],
            'outline_url': data['outline_url'],
            'raw_html': data['raw_html']
        }
    }
    return formatted_data
