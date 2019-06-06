import json
import requests

result_list = {

    ('香港', 1): '中国', ('台湾', 1): '中国', ('澳门', 2): '中国', ('首尔', 1): '韩国', ('釜山', 2): '韩国', ('济州', 2): '韩国',
    ('东京', 1): '日本', ('箱根', 3): '日本', ('伊豆', 3): '日本', ('汤布院', 3): '日本', ('名古屋', 3): '日本', ('轻井泽', 3): '日本',
    ('大阪', 1): '日本', ('热海', 3): '日本', ('京都', 1): '日本', ('富士河口', 3): '日本', ('函馆', 3): '日本', ('长滩岛', 3): '菲律宾',
    ('马尼拉', 4): '菲律宾', ('宿务', 3): '菲律宾', ('芽庄', 2): '越南', ('美奈', 3): '越南', ('岘港', 2): '越南', ('西贡', 2): '越南',
    ('河内', 2): '越南', ('金边', 3): '柬埔寨', ('暹粒', 3): '柬埔寨', ('曼谷', 1): '泰国', ('芭提雅', 2): '泰国', ('清迈 ', 2): '泰国',
    ('普吉岛', 2): '泰国', ('苏梅岛', 2): '泰国', ('甲米', 3): '泰国', ('华欣', 3): '泰国', ('吉隆坡', 2): '马来西亚', ('沙巴', 3): '马来西亚',
    ('槟城', 0): '马来西亚', ('新加坡', 1): '新加坡', ('巴厘岛', 1): '印度尼西亚', ('龙目岛', 3): '印度尼西亚', ('雅加达', 3): '印度尼西亚',
    ('泗水', 0): '印度尼西亚', ('马尔代夫', 3): '马尔代夫', ('迪拜', 2): '阿联酋', ('阿布扎比', 3): '阿联酋', ('伊斯坦布尔', 2): '土耳其',
    ('伊兹密尔', 3): '土耳其', ('安塔利亚', 3): '土耳其', ('卡萨布兰卡', 3): '摩洛哥', ('马拉喀什', 3): '摩洛哥', ('瓦尔扎扎特', 3): '摩洛哥',
    ('非斯', 3): '摩洛哥', ('舍夫沙万', 3): '摩洛哥', ('塞班', 3): '塞班', ('赛舌儿', 3): '赛舌儿', ('毛里求斯', 3): '毛里求斯', ('斐济', 3): '斐济',
    ('大溪地', 3): '大溪地'

}

city_level_num = {1: '300', 2: '200', 3: '150'}


def start_request(city_level, country):
    # url = "http://127.0.0.1:4010/api/v1/taspider"
    url = "http://172.16.4.110:4010/api/v1/taspider"
    city = city_level[0]
    city_level = city_level[1]
    allow_num = city_level_num.get(city_level)
    payload = {
        "city": city,
        "country": country,
        "allow_num": allow_num,
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
