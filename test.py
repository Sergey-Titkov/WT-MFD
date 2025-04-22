import json

test = [
    {"baund": 70, "style": "fill: rgb(0, 157, 2); font-size: 20px; font-family: Arial"},
    {"baund": 70, "style": "fill: rgb(0, 157, 2); font-size: 20px; font-family: Arial"},
    {"baund": 70, "style": "fill: rgb(0, 157, 2); font-size: 20px; font-family: Arial"}
]
print(json.dumps(test, ensure_ascii=False))
