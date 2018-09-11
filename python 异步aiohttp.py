import asyncio
import aiohttp
import time

start = time.time()


async def get(url):
	session = aiohttp.ClientSession()
	response = await session.get(url)
	# 代码里面我们使用了 await，后面跟了 get() 方法，在执行这五个协程的时候，如果遇到了 await，那么就会将当前协程挂起，转而去执行其他的协程，直到其他的协程也挂起或执行完毕，再进行下一个协程的执行。
	result = await response.text()
	session.close()
	return result


async def request():
	url = 'https://www.baidu.com/'
	print('Waiting for', url)
	result = await get(url)


# print('Get response from', url, 'Result:', result)


tasks = [asyncio.ensure_future(request()) for _ in range(1000)]  # 可以创建一个task
loop = asyncio.get_event_loop()
# 使用 get_event_loop() 方法创建了一个事件循环 loop，并调用了 loop 对象的 run_until_complete() 方法将协程注册到事件循环 loop 中，然后启动。
loop.run_until_complete(asyncio.wait(tasks))

end = time.time()
print('Cost time:', end - start)
