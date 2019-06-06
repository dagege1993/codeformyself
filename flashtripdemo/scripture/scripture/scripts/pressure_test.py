#! python
# coding: utf8

import os
from lxml import etree

import asyncio
import aiohttp
from aioutils import Pool

# host = '' or os.environ.get('DHOST')
# con_requests = os.environ.get('CON_REQUESTS') or 5


async def make_request(host, request):
    async with request.get(host) as resp:
        html = await resp.text()
        status = resp.status
        et = etree.HTML(html)
        title = et.xpath('//head/title/text()')
        print(f'Status: {status}, Title: {title}')  # noqa
        del et
    return


async def start(loop, task, host):
    async with aiohttp.ClientSession() as request:
        while True:
            try:
                task.spawn(make_request(host, request))
                await asyncio.sleep(0)
            except KeyboardInterrupt:
                break
    loop.close()


def main(host, con_requests=5):
    loop = asyncio.get_event_loop()
    task = Pool(pool_size=con_requests, loop=loop)
    loop.run_until_complete(start(loop, task, host))
    task.join()
