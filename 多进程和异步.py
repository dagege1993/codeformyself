# 异步请求库库aiohttp,使用 requests 库来进行请求的话，如果网站响应速度过慢，程序一直在等待网站响应，最后导致其爬取效率是非常非常低的。
# 为了解决这类问题，本文就来探讨一下 Python 中异步协程来加速的方法，此种方法对于 IO 密集型任务非常有效。
# import asyncio  # 协程库
# import aiohttp  # 异步请求库
# import time
#
# start = time.time()
#
#
# async def get(url):
#     session = aiohttp.ClientSession()
#     response = await session.get(url)
#     result = await response.text()
#     session.close()
#     return result
#
#
# async def request():
#     url = 'http://127.0.0.1:5000'
#     print('Waiting for', url)
#     result = await get(url)
#     print('Get response from', url, 'Result:', result)
#
#
# tasks = [asyncio.ensure_future(request()) for _ in range(5)]
# loop = asyncio.get_event_loop()
# loop.run_until_complete(asyncio.wait(tasks))
#
# end = time.time()
# print('Cost time:', end - start)

# 多进程multiprocessing还是用request进行请求
import requests
import time
import multiprocessing
#
# start = time.time()
#
#
# def request():
#     url = 'http://127.0.0.1:5000'
#     print('Waiting for', url)
#     result = requests.get(url).text
#     print('Get response from', url, 'Result:', result)
#
#
# cpu_count = multiprocessing.cpu_count()
# print('Cpu count:', cpu_count)
# pool = multiprocessing.Pool(cpu_count)
# pool.map(request, range(100))
#
# end = time.time()
# print('Cost time:', end - start)
import os
from multiprocessing import Pool
import requests
from requests.exceptions import ConnectionError


# 如果你现在有一堆数据要处理，每一项都需要经过一个方法来处理，那么map非常适合。
def scrape(url):
    try:
        print(requests.get(url))
    except ConnectionError:
        print('Error Occured ', url)
    finally:
        print('URL ', url, ' Scraped')


if __name__ == '__main__':
    start = time.time()
    pool = Pool()  # 在这里初始化一个Pool，指定进程数为3，如果不指定，那么会自动根据CPU内核来分配进程数。
    urls = [
        'https://www.baidu.com',
        'http://www.meituan.com/',
        'http://blog.csdn.net/',
        'http://xxxyxxx.net'
    ]
    pool.map(scrape, urls)  # 有一个链接列表，map函数可以遍历每个URL，然后对其分别执行scrape方法。
    end = time.time()
    print('Cost time:', end - start)
    print(os.cpu_count())

    # for i in urls:
    #     scrape(i)
    # end = time.time()
    # print('Cost time:', end - start)
