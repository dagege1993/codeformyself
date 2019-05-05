import hashlib
import requests

url = "https://appdelivery.starbucks.com.cn/assortment/store/list"
payload = "{\"in_business\":1,\"latitude\":\"39.907098\",\"longitude\":\"116.429323\"}"
to_encode = "appid=859977c6f22b4f9ce98d4b02d031b4a8&lang=zh_CN" + payload

# hash = hashlib.sha256()
# hash.update(bytes(to_encode, encoding='utf-8'))
# sign = hash.hexdigest()
# print(sign)

shab1 = hashlib.sha1()
shab1.update(bytes(to_encode, encoding='utf-8'))
sign = shab1.hexdigest()
print("sha1采用byte转换的结果:", sign)

# sign = sha256(to_encode.encode('utf8'))
# print(sign)
# print(len(sign))
querystring = {"lang": "zh_CN", "appid": "859977c6f22b4f9ce98d4b02d031b4a8", "sign": sign}
print(querystring)
headers = {
    'Content-Type': "application/json",
    'Authorization': "Bearer erJCQ3JZMbAAcTinU5JMjcRHdl68e5Om.4oDCinNVwzRNp2x6VF%2FIOd0Qydp9sQk4MWHZQjc5Yxo",
    'cache-control': "no-cache"
}
response = requests.request("POST", url, data=payload, headers=headers, params=querystring)
print(response.text)
