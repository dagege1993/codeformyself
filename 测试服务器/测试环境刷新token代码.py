import requests
import json

url = 'http://192.168.108.30:8089/duolabao/refreshToken'

datas = {}
datas['refreshToken'] = '81ba0cc7-d835-494e-a028-b6cc91597b95'
datas['customerOpenId'] = 'c1852d65eec745d728a84de38b08293a'
datas['cooperatorId'] = '20000004'
headers = {}

response = requests.post(url, data=datas)

print(response.text)
data = json.loads(response.text).get('data')
print(data)
