# 获取公示历史数据
import json
import requests

detail_list = []


# 获取总共的期数
def public_total():
    url = "https://api.shuidihuzhu.com/api/hz/noticeV2/noticeGroupHistory"
    querystring = {"pageNo": 1}
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
    # 首先拿到第一页的数据
    for i in range(1, 100):
        querystring["pageNo"] = i
        response = requests.request("GET", url, headers=headers, params=querystring)
        response_test = json.loads(response.text)
        data = response_test.get('data')
        group_history = data.get('noticeGroupHistoryList')
        for times in group_history:  # 因为group_history是个列表
            year = times.get('year')
            for group in times.get('noticeGroupHistoryDetailVOList'):
                group['year'] = year
                detail_list.append(group)
        pageNo_remote = data.get('pageNo')  # 这个值只是来判断是否结束循环
        print('循环列表', detail_list)
        if pageNo_remote == 0:
            # return len(detail_list)
            return detail_list


# 获取最近一个月的历史数据,看看最近有几期
def public_recent():
    url = "https://api.shuidihuzhu.com/api/hz/noticeV2/noticeGroupHistory"
    querystring = {"pageNo": 1}
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
    response = requests.request("GET", url, headers=headers, params=querystring)
    response_test = json.loads(response.text)
    data = response_test.get('data')
    group_history = data.get('noticeGroupHistoryList')
    for times in group_history:  # 因为group_history是个列表
        year = times.get('year')
        for group in times.get('noticeGroupHistoryDetailVOList'):
            group['year'] = year
            detail_list.append(group)
    return detail_list

# if __name__ == '__main__':
#     print(public_recent())
