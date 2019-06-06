import json
import requests

result_list = {

    ('东京', 1): '日本',
    ('京都市', 1): '日本',
    ('大阪', 1): '日本',

}

city_level_num = {1: '3000', 2: '200', 3: '150'}


def start_request(city_level, country):
    url = "http://127.0.0.1:4010/api/v1/taspider"
    # url = "http://172.16.4.110:4010/api/v1/taspider"
    city = city_level[0]
    city_level = city_level[1]
    allow_num = city_level_num.get(city_level)
    payload = {
        "city": city,
        "country": country,
        "allow_num": allow_num,
        "lost_city": '0',  # 0代表抓取的是缺失城市,1代表的是抓取的是正常城市

    }
    print(city, country)
    payload = json.dumps(payload)
    headers = {
        'Content-Type': "application/json",
        'User-Agent': "PostmanRuntime/7.11.0",
        'Accept': "*/*",
        'Cache-Control': "no-cache",
        'Postman-Token': "dbec0786-3a5e-4966-860f-9276d4503818,4efeb62b-5683-4ddc-9903-bbf88b86c8e3",
        'Host': "127.0.0.1:4010",
        'accept-encoding': "gzip, deflate",
        'content-length': "61",
        'Connection': "keep-alive",
        'cache-control': "no-cache"
    }

    response = requests.request("POST", url, data=payload, headers=headers)

    print(response.text)


for city, country in result_list.items():
    start_request(city, country)
