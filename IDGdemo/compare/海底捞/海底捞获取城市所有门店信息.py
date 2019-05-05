import requests

url = "https://superapp.kiwa-tech.com/app/getNearbyStore"

payload = ""
headers = {
    'X-Ca-Timestamp': "1546509574438",
    'X-Device-Id': "XAPwegaf/twDANyDN1Y1/EVQ",
    'X-App-Version': "6.1.0",
    'X-Ca-Key': "60022326",
    'X-OS-Version': "6.0.1",
    'X-Device-Model': "Phone",
    'X-Ca-Signature-Headers': "X-Ca-Timestamp,X-Ca-Nonce,X-Ca-Key",
    'user-agent': "MI 5(Android/6.0.1) Haidilao(Haidilao/6.1.0) Weex/0.18.17.71 1080x1920",
    '_HAIDILAO_APP_TOKEN': "",
    'X-Ca-Signature': "tIAXk1uM/QBOMUyfRh5FExvTBVe9glUbCayoKRYa7eY=",
    'X-Ca-Nonce': "jahL2U4SM9vN2A3KLmGobzSwaRSFKMxG",
    'X-OS-Type': "Android",
    'X-Source': "app",
    'X-utdid': "",
    'Accept': "application/json; charset=utf-8",
    'Content-Type': "application/json; charset=UTF-8",
    'Content-Length': "57",
    'Host': "superapp.kiwa-tech.com",
    'Connection': "Keep-Alive",
    'Accept-Encoding': "gzip",
    'Cookie': "acw_tc=7b39758215465034827633834e8ec826f8e55dc16bdaa699533d4e2cfdc909",
    'cache-control': "no-cache",
}

response = requests.request("POST", url, data=payload, headers=headers)

print(response.text)
