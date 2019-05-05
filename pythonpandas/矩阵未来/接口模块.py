# encoding=utf8
import json
import time
from flask import Flask
from flask import request

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    return '<h1>hello</h1>'


@app.route('/add', methods=['POST'])
def add():
    data = request.json
    print(data)
    value_array = data.get("value_array")
    value_result = 0
    for value in value_array:
        values = list(value.values())
        value_result += int(values[0])
    print(value_result)
    return_result = {}
    return_result["result"] = value_result
    return_result = json.dumps(return_result)
    return return_result


@app.route('/get_date', methods=['GET'])
def get_date():
    result_date = time.strftime('%Y.%m.%d', time.localtime(time.time()))
    # result = {}
    # result["date"] = result_date
    result = dict(date=result_date)

    return_result = json.dumps(result)
    return return_result


@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    msg = data.get("msg")
    if "您好" in msg and "再见" in msg:
        return_msg = "天气不错。"
    elif "您好" in msg:
        return_msg = "您好，您吃了吗？"
    elif "再见" in msg:
        return_msg = "回见了您内。"

    result = dict(msg=return_msg)
    return_result = json.dumps(result, ensure_ascii=False)
    return return_result


if __name__ == '__main__':
    app.run(port=5000)
