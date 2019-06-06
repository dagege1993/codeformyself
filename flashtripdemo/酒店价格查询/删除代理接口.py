import json

import requests

payload = {'website': 'tripadvisor', 'proxy': '221.239.86.26:32228'}

url = "http://172.16.4.110:4010/api/v1/proxy"
# payload = {"website": "tripadvisor"}
# payload['proxy'] = proxy
# payload = json.dumps(payload)
payload = json.dumps(payload)
print(payload)
delete_response = requests.request("GET", url, data=payload)

print(delete_response)
