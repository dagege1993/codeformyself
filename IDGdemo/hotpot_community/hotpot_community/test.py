import requests

url = "https://superapp.kiwa-tech.com/app/activity/participatePrizes/recommendPage"

payload = ""
headers = {
    'X-Device-Model': "Phone",
    'user-agent': "MI 5(Android/6.0.1) Haidilao(Haidilao/6.1.0) Weex/0.18.17.71 1080x1920",
    'X-OS-Type': "Android",
    'X-Source': "app",
    'Accept': "application/json; charset=utf-8",
    'Content-Type': "application/x-www-form-urlencoded",
    'Content-Length': "79",
    'Host': "superapp.kiwa-tech.com",
    'Connection': "Keep-Alive",
    'Accept-Encoding': "gzip",
    'cache-control': "no-cache",
    'Postman-Token': "33372b39-c5cb-437c-a4cd-d0355d622fed"
}

response = requests.request("POST", url, data=payload, headers=headers)

print(response.text)