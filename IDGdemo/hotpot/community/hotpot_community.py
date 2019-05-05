import json

import requests


def get_community_first():
    url = "https://superapp.kiwa-tech.com/app/activity/participatePrizes/recommendPage"

    payload = "{\"_HAIDILAO_APP_TOKEN\":\"\",\"customerId\":\"\",\"limit\":10,\"topicIds\":\"\",\"topSign\":0}"
    headers = {
        'X-Ca-Timestamp': "1550646871944",
        'X-Device-Id': "XAPwegaf/twDANyDN1Y1/EVQ",
        'X-App-Version': "6.1.0",
        'X-Ca-Key': "60022326",
        'X-OS-Version': "6.0.1",
        'X-Device-Model': "Phone",
        'X-Ca-Signature-Headers': "X-Ca-Timestamp,X-Ca-Nonce,X-Ca-Key",
        'user-agent': "MI 5(Android/6.0.1) Haidilao(Haidilao/6.1.0) Weex/0.18.17.71 1080x1920",
        '_HAIDILAO_APP_TOKEN': "",
        'X-Ca-Signature': "gIe7FiJFQtespiA9R/Ce1NlHrj0tqPLfhN+TTmXGLnE=",
        'X-Ca-Nonce': "lB0RBdtxTQ0FxS9k0TnjIgLLr1zg6YM0",
        'X-OS-Type': "Android",
        'X-Source': "app",
        'X-utdid': "",
        'Accept': "application/json; charset=utf-8",
        'Content-Type': "application/json; charset=UTF-8",
        'Content-Length': "79",
        'Host': "superapp.kiwa-tech.com",
        'Connection': "Keep-Alive",
        'Accept-Encoding': "gzip",
        'Cookie': "acw_tc=7b39758815499358044523426ec912897232ac1205f53dec3c36ec43c85ece",
        'cache-control': "no-cache",
        'Postman-Token': "21602650-2745-44a8-8a22-676958c36afc"
    }
    response = requests.request("POST", url, data=payload, headers=headers)
    print(response.text)
    response_text = json.loads(response.text)
    data = response_text.get('data')
    data_list = data.get('data')
    for data in data_list:
        memberOutVo = data.get('memberOutVo')
        customerId = memberOutVo.get('userId')
        userName = memberOutVo.get('userName')
        print(customerId, userName)
        # 传入用户ID
        get_follw(customerId)


# 获取粉丝列表页
def get_follw(customerId):
    url = "https://superapp.kiwa-tech.com/app/homepage/othersFollow"

    payload = {"_HAIDILAO_APP_TOKEN": "TOKEN_APP_c0c315cc-494c-4558-98fb-cd3e6bfe20e7", "customerId": "n-13000488",
               "othersId": "1-6758589644", "operType": 1}
    payload["customerId"] = customerId
    payload = json.dumps(payload)
    headers = {
        'X-Device-Id': "XAPwegaf/twDANyDN1Y1/EVQ",
        'X-App-Version': "6.1.0",
        'X-Ca-Key': "60022326",
        'X-OS-Version': "6.0.1",
        'X-Device-Model': "Phone",
        'X-Ca-Signature-Headers': "X-Ca-Timestamp,X-Ca-Nonce,X-Ca-Key",
        'user-agent': "MI 5(Android/6.0.1) Haidilao(Haidilao/6.1.0) Weex/0.18.17.71 1080x1920",
        '_HAIDILAO_APP_TOKEN': "TOKEN_APP_c0c315cc-494c-4558-98fb-cd3e6bfe20e7",
        'X-OS-Type': "Android",
        'X-Source': "app",
        'X-utdid': "",
        'Accept': "application/json; charset=utf-8",
        'Content-Type': "application/json; charset=UTF-8",
        'Host': "superapp.kiwa-tech.com",
        'Connection': "Keep-Alive",
        'Accept-Encoding': "gzip",
        'Cookie': "_HAIDILAO_APP_TOKEN=TOKEN_APP_c0c315cc-494c-4558-98fb-cd3e6bfe20e7; acw_tc=7b39758815499358044523426ec912897232ac1205f53dec3c36ec43c85ece",
        'cache-control': "no-cache",
        'Postman-Token': "77ddd3a4-43b5-4a43-916d-8c9f95a0a601"
    }

    response = requests.request("POST", url, data=payload, headers=headers)

    # print(response.text)
    response_text = json.loads(response.text)
    data = response_text.get('data')
    data_list = data.get('data')
    for data in data_list:
        customerId = data.get('customerId')
        customerName = data.get('customerName')
        print(customerId, customerName)
        # 回调自身
        get_follw(customerId)


if __name__ == '__main__':
    get_community_first()
