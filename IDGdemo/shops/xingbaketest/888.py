
import requests
from urllib import parse
url = "https://appdelivery.starbucks.com.cn/assortment/menu/detail"

querystring = {"store_id": "25023", "lang": "zh-cn", "appid": "859977c6f22b4f9ce98d4b02d031b4a8",
               "sign": "mcOSiT9YT7246yLUxPIa9bPvHtjWVJn%2Fmp90Kdk3H%2F9BG72vriVEHmfQBnXrSaRs1Wpm%2B%2Bct9hIY%0AnX7X%2BmTSi%2BuLJNtcl331d7pWrl%2Bu6R42lZ9Agl3ISCPes0RqEyyWGyGpI2KSeK1EKK7eLOgelxMb%0A%2FlYRhZqVkj2BVV5foHtAwAI5m0Pls8%2BShPuI0mTQPbQqW3S2j%2Fii68VmpIXddCU6yAw02sZG7%2BrE%0AlJHL5EvG5ybdC881LO1i0YPIWhkW6tUL4G%2FB7y3pzEkICRX5ium4HHMaoIYjz4PjTJtW6qM0gYZG%0Aqr6djRfRts%2F8d5pEZsrnOryskKOpd%2F3XW0lSfA%3D%3D%0A%0A"}
result = querystring["sign"]
result = parse.unquote(result)
print(result)

querystring["sign"] = result
payload = ""
headers = {
    'Host': "appdelivery.starbucks.com.cn",
    'Connection': "Keep-Alive",
    'Accept-Encoding': "gzip",
    'Authorization': "Bearer cgYh7tam3VW6AJjd8fnnFNuWbwTw26oC.lDdNN9X8G7%2FGZ%2Fvwscl69Aeqd%2BxwL57CLVF4aavf%2FD8",
    'User-Agent': "com.starbucks.cn/2157",
    'x-bs-device-id': "kpOv8udkAryBA3OfoBOe_XAn46tmIT7EZXIsIFi0KzffmyKGX-YpIZ5b2ULurX_HF0Ra3Ki8gVT_UiXQMcLX_WwAl0e5ZQ6GFAS7je-TGaA3QLNCu7aEgAwY9jfEbsQG9NmcsK-HX6onu_gpcIfEn6nrAjXWY14F",
    'cache-control': "no-cache",
    'Postman-Token': "2db8226b-b9c9-41ea-9e47-1d1d1135ef37"
}

response = requests.request("GET", url, data=payload, headers=headers, params=querystring)

print(response.text)
