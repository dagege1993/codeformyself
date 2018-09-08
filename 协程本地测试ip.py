import aiohttp
import asyncio

import requests

VALID_STATUS_CODES = [200, 302]
conn = aiohttp.TCPConnector(verify_ssl=False)  # 同时最大进行连接的连接数为30，默认是100，limit=0的时候是无限制
from faker import Faker

f = Faker(locale='zh_CN')


# 对于有的网站，需要验证证书，比如：12306。verify_ssl 默认是验证的,直接关掉
async def test_single_proxy(self):
	"""
	测试单个代理
	:param proxy:
	:return:
	"""
	conn = aiohttp.TCPConnector(verify_ssl=False)  # 同时最大进行连接的连接数为30，默认是100，limit=0的时候是无限制
	# 对于有的网站，需要验证证书，比如：12306。verify_ssl 默认是验证的,直接关掉
	async with aiohttp.ClientSession(connector=conn) as session:
		try:
			
			url = 'http://192.168.107.38:5555/qichacha/random'
			response = requests.get(url)
			
			real_proxy = 'http://' + response.text
			test_url = 'https://www.qichacha.com/'
			async with session.get(test_url, proxy=real_proxy, allow_redirects=False, timeout=15,
			                       headers={'User-Agent': f.chrome()}) as response:
				if response.status in VALID_STATUS_CODES:
					
					print('代理可用', real_proxy)
				
				else:
					print('请求响应码不合法 ', response.status, 'IP', real_proxy)
		except Exception as e:
			print('测试器发生错误', e.args)


if __name__ == '__main__':
	test_single_proxy()
	loop = asyncio.get_event_loop()  # asyncio.get_event_loop方法可以创建一个事件循环，
	tasks = [test_single_proxy()]  # 生成一个任务列表
	# asyncio.wait(tasks) 也可以使用 asyncio.gather(*tasks) ,前者接受一个task列表，后者接收一堆task
	loop.run_until_complete(asyncio.wait(tasks))  # 然后使用run_until_complete将协程注册到事件循环，并启动事件循环。
