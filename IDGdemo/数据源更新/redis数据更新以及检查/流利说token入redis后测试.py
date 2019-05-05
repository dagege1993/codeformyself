import requests
import redis

r = redis.StrictRedis(host='192.168.103.31', decode_responses=True)
token_list = r.lrange("token", 0, -1)
# print(token_list)
# print(len(token_list))
for token in token_list:
    url = "https://apineo.llsapp.com/api/v1/curriculums/3-cccccccccccccccccccccccc"
    querystring = {"appVer": "6", "clientAppVersion": "5.", "token": "6ff2fce0cf5b0136652b0a5864605265",
                   "deviceId": "354730011088642", "sDeviceId": "354730010301566", "appId": "lls",
                   "orderSourceType": "1"}
    querystring["token"] = token
    payload = ""
    headers = {
        'cache-control': "no-cache",
        'Postman-Token': "3f90c4d1-f3c8-4199-829c-7ed893a99274"
    }

    response = requests.request("GET", url, data=payload, headers=headers, params=querystring, verify=False)

    # print(response.text)
    if '未登录' in response.text:
        print(token)
        r.lrem('token', count=0, value=token)
