import requests

url = 'http://192.168.107.38:5555/liepins/random'
response = requests.get(url)

proxy = 'http://' + response.text
print(proxy)
