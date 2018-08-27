import requests
from faker import Faker
from requests.adapters import HTTPAdapter

f = Faker(locale='zh_CN')
test_url = 'http://guangzhou.11467.com/luogangqu/s752/'
for k in range(1, 10000):
	
	headers = {
		'User-Agent': f.chrome()}
	
	try:
		s = requests.Session()   # 保持请求之间的Cookies
		s.mount('http://', HTTPAdapter(max_retries=3))
		response = s.get(test_url, headers=headers, timeout=1)
	except Exception as e:
		print(k, e)

# s = requests.Session()
# s.mount('http://', HTTPAdapter(max_retries=3))
# response = s.get(test_url, headers=headers, proxies=proxies, timeout=1)
