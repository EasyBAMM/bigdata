import json


def open_json_file():

    with open("samplejson.json", "r", encoding="utf-8") as f:
        json_data = json.load(f)


def save_json_file():

    response = {"hello": "world", "hell2": 1234}

    with open('samplejson2.json', 'w', encoding="utf-8") as make_file:
        json.dump(response, make_file, indent="\t", ensure_ascii=False)
