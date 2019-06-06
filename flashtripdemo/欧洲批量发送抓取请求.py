import json
import requests

result_list = {

    ('伦敦', 1): '英国',
    # ('罗马', 1): '意大利', ('威尼斯', 1): '意大利',
    # ('巴黎', 1): '法国',
    # ('拉孔达米讷', 1): '摩纳哥',
    # ('蒙特卡洛', 1): '摩纳哥',
    # ('戛纳', 1): '法国', ('尼斯', 1): '法国', ('普罗旺斯', 1): '法国', ('阿维尼翁', 1): '法国', ('巴塞罗那', 1): '西班牙',

    # ('剑桥', 2): '英国', ('牛津', 2): '英国', ('巴斯', 2): '英国', ('苏格兰高地', 2): '英国', ('爱丁堡', 2): '英国',
    # ('慕尼黑', 2): '德国', ('柏林', 2): '德国', ('法兰克福', 3): '德国',
    # ('马德里', 2): '西班牙',('塞维利亚', 2): '西班牙',
    # ('圣托里尼', 2): '希腊', ('雅典', 2): '希腊', ('扎金索斯', 3): '希腊',
    # ('米克诺斯', 3): '希腊',
    # ('佛罗伦萨', 2): '意大利', ('米兰', 2): '意大利', ('托斯卡纳', 2): '意大利',
    # ('五渔村', 2): '意大利', ('拉斯佩齐亚', 3): '意大利', ('奥斯陆', 2): '挪威', ('卑尔根', 3): '挪威', ('特罗姆瑟', 3): '挪威',
    # ('雷克雅未克', 3): '冰岛', ('斯德哥尔摩', 3): '瑞典', ('赫尔辛基', 3): '芬兰', ('罗瓦涅米', 3): '芬兰', ('哥本哈根', 3): '丹麦',
    # ('布拉格', 2): '捷克', ('维也纳', 2): '奥地利', ('萨尔茨堡', 3): '奥地利', ('因特拉肯', 3):
    #     '瑞士', ('卢塞恩', 3): '瑞士', ('苏黎世', 2): '瑞士', ('日内瓦', 2): '瑞士', ('采尔马特', 3): '瑞士',
    # ('布达佩斯', 2): '匈牙利', ('里斯本', 3): '葡萄牙', ('布鲁塞尔', 2): '比利时', ('阿姆斯特丹', 2): '荷兰', ('鹿特丹', 3): '荷兰'

}

city_level_num = {1: '300', 2: '200', 3: '150'}


def start_request(city_level, country):
    url = "http://127.0.0.1:4010/api/v1/taspider"
    # url = "http://172.16.4.110:4010/api/v1/taspider"
    city = city_level[0]
    city_level = city_level[1]
    allow_num = city_level_num.get(city_level)
    # if allow_num == '300':  # and city == '伦敦'
    payload = {
        "city": city,
        "country": country,
        "allow_num": allow_num,
        "lost_city": '0'  # 0代表抓取的是缺失城市,1代表的是抓取的是正常城市
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


# for i in range(10):
#     for city, country in result_list.items():
#         # print(city, country)
#         start_request(city, country)


for city, country in result_list.items():
    start_request(city, country)
