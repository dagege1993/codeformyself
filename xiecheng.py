import aiohttp
import asyncio

import requests

VALID_STATUS_CODES = [200, 302]
conn = aiohttp.TCPConnector(verify_ssl=False)  # 同时最大进行连接的连接数为30，默认是100，limit=0的时候是无限制
from faker import Faker

f = Faker(locale='zh_CN')

# 对于有的网站，需要验证证书，比如：12306。verify_ssl 默认是验证的,直接关掉
# async def test_single_proxy():
# 	conn = aiohttp.TCPConnector(verify_ssl=False)  # 同时最大进行连接的连接数为30，默认是100，limit=0的时候是无限制
# 	# 对于有的网站，需要验证证书，比如：12306。verify_ssl 默认是验证的,直接关掉
# 	async with aiohttp.ClientSession(connector=conn) as session:
# 		try:
#
# 			url = 'http://192.168.107.38:5555/qichacha/random'
# 			response = requests.get(url)
# 			real_proxy = 'http://' + response.text
# 			test_url = 'https://www.qichacha.com/'
# 			async with session.get(test_url, proxy=real_proxy, allow_redirects=False, timeout=15,
# 			                       headers={'User-Agent': f.chrome()}) as response:
# 				if response.status in VALID_STATUS_CODES:
#
# 					print('代理可用', real_proxy)
#
# 				else:
# 					print('请求响应码不合法 ', response.status, 'IP', real_proxy)
# 		except Exception as e:
# 			print('测试器发生错误', e.args)


if __name__ == '__main__':
	# print(1111)
	# test_single_proxy()
	for i in range(1, 100):
		url = 'http://192.168.107.38:5555/qichacha/random'
		response = requests.get(url)
		# print(response)
		ip = response.text
		real_proxy = {
			'http': 'http://' + response.text,
			'https': 'https://' + response.text,
		}
		
		test_url = 'https://www.qichacha.com/'
		try:
			response = requests.get(test_url, proxies=real_proxy)
			print(response.text)
		except Exception as e:
			url = 'http://192.168.107.38:5555/qichacha/' + ip + '/del'
			response = requests.get(url)
			print(response)
