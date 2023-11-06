import json


def double_json_stringify(data) -> str:
    return json.dumps([None, json.dumps(data)])
