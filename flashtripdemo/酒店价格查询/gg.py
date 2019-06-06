import requests

url = "http://127.0.0.1:4010/api/v1/data/publish/availability"

payload = "{\n    \"start_time\": \"2019-06-24\",\n    \"days\": 2,\n    \"compare\":[\"ctrip\"],\n    \"hotels\": [\"cms::5942913a7157f7428fe4eccc\"],\n}"
headers = {
    'Content-Type': "application/json",
    'User-Agent': "PostmanRuntime/7.11.0",
    'Accept': "*/*",
    'Cache-Control': "no-cache",
    'Postman-Token': "97550480-c43d-4cc7-8cdb-770860a65851,b804ff13-2a5f-4345-95b6-59b65f94c4b1",
    'Host': "127.0.0.1:4010",
    'accept-encoding': "gzip, deflate",
    'content-length': "124",
    'Connection': "keep-alive",
    'cache-control': "no-cache"
    }

response = requests.request("POST", url, data=payload, headers=headers)

print(response.text)