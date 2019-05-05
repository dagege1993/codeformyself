import json
import math
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
    url = "http://apineo.llsapp.com/api/v1/podcasts"
    querystring = {"page": "1", "appId": "lls", "deviceId": "354730010301566", "sDeviceId": "354730010301566",
                   "appVer": "4", "token": "0465e280c892013659dc0a5864630fa3"}
    querystring['token'] = get_token()
    payload = ""
    headers = {
        'cache-control': "no-cache",
    }
    response = requests.request("GET", url, data=payload, headers=headers, params=querystring)
    response_text = json.loads(response.text)
    total = response_text.get('total')
    max_page = math.ceil(total / 20)  # 向上取整
    max_page += 1
    user_list = []
    for page in range(1, int(max_page)):
        querystring['page'] = page
        response = requests.request("GET", url, data=payload, headers=headers, params=querystring)
        response_text = json.loads(response.text)
        podcasts = response_text.get('podcasts')
        for user in podcasts:
            user_id = user.get('user').get('id')
            user_url = "http://apineo.llsapp.com/api/v1/users/" + user_id + "/profile?appId=lls&deviceId=354730011650847&sDeviceId=354730010301566&appVer=4&token=" + get_token()
            user_list.append(user_url)
    print('初始用户维度', len(user_list))

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
