from faker import Faker
from requests.adapters import HTTPAdapter
import requests

f = Faker(locale='zh_CN')
url = 'http://192.168.107.38:5555/58/random'
response = requests.get(url)

proxy = response.text
print(proxy)
proxies = {
	# "http": "http://" + proxy,
	# "https": "http://" + proxy,
	"http": "http://" + "117.80.147.117:2589",
	"https": "http://" + "117.80.147.117:2589",
	# "http": "http://" + "112.113.153.160:4242",
	# "https": "http://" + "112.113.153.160:4242",
}
print(proxies)
headers = {
	'User-Agent': f.chrome()}

# for i in range()
try:
	s = requests.Session()
	s.mount('http://', HTTPAdapter(max_retries=3))
	response = s.get("https://cn.58.com/", headers=headers, proxies=proxies, timeout=2)
	print(111)
except Exception as e:
	url = 'http://192.168.107.38:5555/58/' + proxy + '/del'
	response = requests.get(url)
	print(response)
