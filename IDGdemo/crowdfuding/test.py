import requests


# APP首页
def get_homepage():
    url = "https://api.shuidihuzhu.com/api/hz/order/v3/allocationSummary"

    payload = ""
    headers = {
        'device-id': "309c237660c13218",
        'app-id': "shuidihuzhu_android",
        'appversion': "1.8.3",
        'app-minorid': "1.8.3",
        'app-time': "1542594401171",
        'api-sign': "85A0793FF230ADF94AD80D6DFEFF0371B20E94C6",
        'user-agent': "[Wifi;OPPO R11;Android;19;720*1280*240;yingyongbao;zh]",
        'callid': "undefined",
        'Content-Type': "application/x-www-form-urlencoded;charset=UTF-8",
        'Content-Length': "121",
        'Host': "api.shuidihuzhu.com",
        'Connection': "Keep-Alive",
        'Accept-Encoding': "gzip",
        'Cookie': "uuid=YnH3aaFHkPS4Rd4rxF51542594296059",
        'cache-control': "no-cache",
        'Postman-Token': "759f4a29-d19d-47d3-b0e0-b61c1238344b"
    }

    response = requests.request("POST", url, data=payload, headers=headers)

    print(response.text)


# 公示首页
def public_homepage():
    url = "https://api.shuidihuzhu.com/api/hz/noticeV2/noticeTab"

    payload = ""
    headers = {
        'Host': "api.shuidihuzhu.com",
        'Connection': "keep-alive",
        'Accept': "application/json, text/plain, */*",
        'Origin': "https://www.shuidihuzhu.com",
        'User-Agent': "Mozilla/5.0 (Linux; Android 4.4.2; OPPO R11 Build/NMF26X) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/30.0.0.0 Mobile Safari/537.36 android rock/1.8.3",
        'api-version': "2",
        'AuthorizationV2': "",
        'Content-Type': "application/x-www-form-urlencoded",
        'Referer': "https://www.shuidihuzhu.com/sd/helpNotice?channel=app_android_yingyongbao_1.8.3&appChannel=app_android_yingyongbao_1.8.3&platform=3&appVersion=1.8.3",
        'Accept-Encoding': "gzip,deflate",
        'Accept-Language': "zh-CN,en-US;q=0.8",
        'X-Requested-With': "com.shuidihuzhu.rock",
        'cache-control': "no-cache",
        'Postman-Token': "c8fdd72e-8063-49e0-b9db-f0b1a725adb7"
    }

    response = requests.request("GET", url, data=payload, headers=headers)

    print(response.text)


# 获取公示历史数据
def public_total():
    url = "https://api.shuidihuzhu.com/api/hz/noticeV2/noticeGroupHistory"

    querystring = {"pageNo": "1"}

    payload = ""
    headers = {
        'Host': "api.shuidihuzhu.com",
        'Connection': "keep-alive",
        'Accept': "application/json, text/plain, */*",
        'Origin': "https://www.shuidihuzhu.com",
        'User-Agent': "Mozilla/5.0 (Linux; Android 4.4.2; OPPO R11 Build/NMF26X) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/30.0.0.0 Mobile Safari/537.36 android rock/1.8.3",
        'api-version': "2",
        'AuthorizationV2': "67vQPM0zeQHq2kvgrb5-gYwdzmeX2qV9Bqgk2wN3PGs=",
        'Content-Type': "application/x-www-form-urlencoded",
        'Referer': "https://www.shuidihuzhu.com/sd/helpNotice/history?channel=app_android_yingyongbao_1.8.3",
        'Accept-Encoding': "gzip,deflate",
        'Accept-Language': "zh-CN,en-US;q=0.8",
        'X-Requested-With': "com.shuidihuzhu.rock",
        'cache-control': "no-cache",
        'Postman-Token': "e21a975c-36d0-4aeb-a088-228ebdadbeba"
    }

    response = requests.request("GET", url, data=payload, headers=headers, params=querystring)

    print(response.text)


# 获取某一期公示详情数据
def public_detail():
    url = "https://api.shuidihuzhu.com/api/hz/noticeV2/userListV2"

    payload = {"groupNo": "62409d911d09c1c55fb4f1",
               "thirdType": "2",
               "AuthorizationV2": "67vQPM0zeQHq2kvgrb5-gYwdzmeX2qV9Bqgk2wN3PGs="}
    headers = {
        'content-type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
        'Host': "api.shuidihuzhu.com",
        'Connection': "keep-alive",
        'Content-Length': "105",
        'Accept': "application/json, text/plain, */*",
        'Origin': "https://www.shuidihuzhu.com",
        'User-Agent': "Mozilla/5.0 (Linux; Android 4.4.2; OPPO R11 Build/NMF26X) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/30.0.0.0 Mobile Safari/537.36 android rock/1.8.3",
        'api-version': "2",
        'AuthorizationV2': "67vQPM0zeQHq2kvgrb5-gYwdzmeX2qV9Bqgk2wN3PGs=",
        'Content-Type': "application/x-www-form-urlencoded",
        'Referer': "https://www.shuidihuzhu.com/sd/notice/8c4b029f7f26d47fd9f1ba?channel=app_android_yingyongbao_1.8.3",
        'Accept-Encoding': "gzip,deflate",
        'Accept-Language': "zh-CN,en-US;q=0.8",
        'X-Requested-With': "com.shuidihuzhu.rock",
        'cache-control': "no-cache",
    }

    response = requests.request("POST", url, data=payload, headers=headers)

    print(response.text)


if __name__ == '__main__':
    # get_homepage()
    # public_homepage()
    # public_total()
    # public_detail()
    ll = '9170622.85'
    print(int(float(ll)))

    # 这段代码功能是字典根据value去重
    d = {'d': 0, 'b': 0, 'c': 1}
    func = lambda z: dict([(x, y) for y, x in z.items()])  # 把字典的key,value翻过来
    print(d)
    print(func(d))
    print(func(func(d)))
