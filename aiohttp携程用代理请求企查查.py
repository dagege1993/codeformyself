import asyncio
import aiohttp
import time

import requests

start = time.time()


def get_proxy():
	url = 'http://192.168.107.38:5555/General_pool/random'
	response = requests.get(url)
	
	proxy = 'http://' + response.text
	if response.status_code == 500:
		return 500
	else:
		return proxy


async def get(url):
	session = aiohttp.ClientSession()
	proxys = get_proxy()
	response = await session.get(url, proxy=proxys)
	response = await session.get(url, proxy='http://218.95.26.116:1863')
	# 代码里面我们使用了 await，后面跟了 get() 方法，在执行这五个协程的时候，如果遇到了 await，那么就会将当前协程挂起，转而去执行其他的协程，直到其他的协程也挂起或执行完毕，再进行下一个协程的执行。
	result = await response.text()
	session.close()
	return result


async def request():
	url = 'https://www.qichacha.com/g_AH'
	url = 'https://www.baidu.com/'
	print('Waiting for', url)
	result = await get(url)
	print('Get response from', url, 'Result:', result)


tasks = [asyncio.ensure_future(request()) for _ in range(10)]  # 可以创建一个task
loop = asyncio.get_event_loop()
# 使用 get_event_loop() 方法创建了一个事件循环 loop，并调用了 loop 对象的 run_until_complete() 方法将协程注册到事件循环 loop 中，然后启动。
loop.run_until_complete(asyncio.wait(tasks))

end = time.time()
print('Cost time:', end - start)

blog = 'https://blog.csdn.net/getcomputerstyle/article/details/71515331'
'''14.设置代理



aiohttp支持使用代理来访问网页：

async with aiohttp.ClientSession() as session:
    async with session.get("http://python.org",
                           proxy="http://some.proxy.com") as resp:
        print(resp.status)
当然也支持需要授权的页面：
async with aiohttp.ClientSession() as session:
    proxy_auth = aiohttp.BasicAuth('user', 'pass')
    async with session.get("http://python.org",
                           proxy="http://some.proxy.com",
                           proxy_auth=proxy_auth) as resp:
        print(resp.status)
或者通过这种方式来验证授权：
session.get("http://python.org",
            proxy="http://user:pass@some.proxy.com")
'''

