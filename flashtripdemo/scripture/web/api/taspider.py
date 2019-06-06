# coding: utf-8
from sanic.response import html
from web.utils.add_compair_task import start_ta_spider, start_ja_spider
from . import api_v1


@api_v1.post('/taspider')
async def ta_spider_star(request):
    body = request.json
    await start_ta_spider(body['city'], body['country'], body['allow_num'], body['lost_city'].body['filter_or_not'])
    return html('<h1>OK</h1>')


@api_v1.get('/japanican')
async def ta_spider_japanican(request):
    await start_ja_spider()
    return html('<h1>OK</h1>')
