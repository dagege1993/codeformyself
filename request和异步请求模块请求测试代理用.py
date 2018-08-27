import requests
from faker import Faker

f = Faker(locale='zh_CN')
url = 'http://b2b.11467.com/search/748.htm'

proxies = {
	'http': 'http://115.221.14.73:2316',
	# 'https': 'http://172.18.101.221:1080',
}

response = requests.get(url, proxies=proxies, headers={'User-Agent': f.chrome()})
print(response.text)

import asyncio
import aiohttp


# 异步请求模块
# async def get(url):
# 	proxies = 'http://117.86.187.228:8736'
# 	session = aiohttp.ClientSession()
# 	response = await session.get(url, proxy=proxies, timeout=5, headers={'User-Agent': f.chrome()})
# 	result = await response.text()
#
# 	session.close()
# 	return result
#
#
# async def request():
# 	url = 'https://www.baidu.com/'
# 	print('Waiting for', url)
# 	result = await get(url)
# 	print('Get response from', url, 'Result:', result)


# tasks = [asyncio.ensure_future(request()) for _ in range(2)]
# loop = asyncio.get_event_loop()
# loop.run_until_complete(asyncio.wait(tasks))


class Tester(object):
	def __init__(self):
		self.redis = 111
	
	async def test_single_proxy(self, proxy):
		"""
		测试单个代理
		:param proxy:
		:return:
		"""
		TEST_URL = 'http://www.baidu.com/'
		VALID_STATUS_CODES = [200, 302]
		
		conn = aiohttp.TCPConnector(verify_ssl=False)
		async with aiohttp.ClientSession(connector=conn) as session:
			try:
				if isinstance(proxy, bytes):
					proxy = proxy.decode('utf-8')
				real_proxy = 'http://' + proxy
				print('real_proxy', real_proxy)
				print('正在测试', proxy)
				async with session.get(TEST_URL, proxy=real_proxy, allow_redirects=False, timeout=15,
				                       headers={'User-Agent': f.chrome()}) as response:
					print('打印response', response.text)
					if response.status in VALID_STATUS_CODES:
						
						print('代理可用', proxy)
					else:
						
						print('请求响应码不合法 ', response.status, 'IP', proxy)
			except (aiohttp.client_exceptions.ClientConnectorError, asyncio.TimeoutError, AttributeError):
				
				print('代理请求失败', proxy)


# proxy = '114.99.12.15:4276'
# proxy = '117.90.2.238:3217'
# test = Tester()
# tasks = [asyncio.ensure_future(test.test_single_proxy(proxy)) for _ in range(2)]
# loop = asyncio.get_event_loop()
# loop.run_until_complete(asyncio.wait(tasks))
