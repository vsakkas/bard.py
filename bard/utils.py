import json
import random


def double_json_stringify(data) -> str:
    return json.dumps([None, json.dumps(data)])


def random_digit_as_string(length: int) -> str:
    return "".join(str(random.randint(0, 9)) for _ in range(length))
