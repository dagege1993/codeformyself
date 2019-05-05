import json
import random
import redis
import requests

url = "http://apineo.llsapp.com/api/v1/podcasts"

querystring = {"page": "10", "appId": "lls", "deviceId": "354730010301566", "sDeviceId": "354730010301566",
               "appVer": "4", "token": "0465e280c892013659dc0a5864630fa3"}

payload = ""
headers = {
    'cache-control': "no-cache",
}

response = requests.request("GET", url, data=payload, headers=headers, params=querystring)

print(response.text)


def start_url_list():
    start_urls = [
        "https://apineo.llsapp.com/api/v1/feeds/recommend?maxId=22044&appVer=6&deviceId=354730010301566&sDeviceId=354730010301566&appId=lls&token=",
        "https://apineo.llsapp.com/api/v1/feeds/recommend?maxId=22008&appVer=6&deviceId=354730010301566&sDeviceId=354730010301566&appId=lls&token=",
        "https://apineo.llsapp.com/api/v1/feeds/recommend?maxId=22044&appVer=6&deviceId=354730010301566&sDeviceId=354730010301566&appId=lls&token=",
        "https://apineo.llsapp.com/api/v1/feeds/recommend?maxId=22008&appVer=6&deviceId=354730010301566&sDeviceId=354730010301566&appId=lls&token=",
    ]
    start_user_list = []
    for start_url in start_urls:
        start_url = start_url + get_token()
        headers = {'cache-control': "no-cache", }
        response = requests.request("GET", start_url, headers=headers)
        response_text = json.loads(response.text)
        feeds = response_text.get('feeds')
        start_user_list.extend(feeds)
    start_user_list = set_list(start_user_list)  # 把列表页去重,返回列表

    user_list = []
    # 去重后的用户页,拼接url,考虑的是首页的用户已经入库,但是他们的粉丝还没入库
    for user in start_user_list:
        user_id = user.get('userId')
        url = "http://apineo.llsapp.com/api/v1/users/" + user_id + "/profile?appId=lls&deviceId=354730011650847&sDeviceId=354730010301566&appVer=4&token=" + get_token()
        user_list.append(url)
    print(user_list)
    return user_list


# 从redis 获取一个随机的token,这个token是设置了7天的过期时间
def get_token():
    conn = redis.StrictRedis(host='192.168.103.31')
    token_len = conn.llen('token')
    result = conn.lindex("token", random.randint(0, token_len - 1))
    result = str(result, encoding="utf8")
    return result


# 对列表包含字典的元素进行去重,返回去重后的列表
def set_list(large_list):
    samll_list = []
    samll_list.append(large_list[0])
    for dict in large_list:
        k = 0
        for item in samll_list:
            if dict['userName'] != item['userName']:
                k = k + 1
            else:
                break
            if k == len(samll_list):
                samll_list.append(dict)

    return samll_list


if __name__ == '__main__':
    start_url_list()
