import requests

url = "http://127.0.0.1:4010/api/v1/data/publish/availability"

payload = "{\n    \"start_time\": \"2019-05-01\",\n    \"days\": 10,\n    \"hotels\": [\"cms::59292a0c78647808cee9527b\"],\n}"
headers = {
    'Content-Type': "application/json",
    'User-Agent': "PostmanRuntime/7.11.0",
    'Accept': "*/*",
    'Cache-Control': "no-cache",
    'Postman-Token': "b58102b0-e939-43fe-8182-844f8052b45d,325ef015-be6b-41f3-a231-667dddc0f59e",
    'Host': "127.0.0.1:4010",
    'accept-encoding': "gzip, deflate",
    'content-length': "100",
    'Connection': "keep-alive",
    'cache-control': "no-cache"
}

response = requests.request("POST", url, data=payload, headers=headers)

print(response.text)
