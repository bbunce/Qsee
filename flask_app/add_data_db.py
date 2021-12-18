import json
import requests


def add_json_manual(json_string):
    """Load data from string in json format"""
    data_json = json.loads(json_string)
    print(data_json)
    r = requests.post('http://127.0.0.1:5000/add/', json=data_json)
    print(f"Record added: {data_json}\nStatus code: {r.status_code}\nJSON format: {r.json()}")


def add_json_file(path):
    """Load data from .json file. Format {"Values":[{record}]}"""
    data = open(path, 'r')
    data_json = json.load(data)
    for value in data_json['Values']:
        r = requests.post('http://127.0.0.1:5000/add/', json=value)
        print(f"Record added: {value}\nStatus code: {r.status_code}\nJSON format: {r.json()}")


json_string = '{"assay_type": "assay_type", "value": 1.0}'
# add_json_manual(json_string)
add_json_file('../tests/data/db_data.json')