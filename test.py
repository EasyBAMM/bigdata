import json
from dotenv import dotenv_values

config = dotenv_values(".env")
print(config['API_KEY'])

hello = {"hello": 123, "world": "beolo"}
json_string = json.dumps(hello)
print(json_string)
if hello['hello']:
    print(hello)


def hello(count=99):
    if count < 1:
        return

    print(count)
    hello(count-1)


hello()
