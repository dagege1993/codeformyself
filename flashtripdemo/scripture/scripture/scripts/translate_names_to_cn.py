# coding: utf-8

import asyncio
import logging
import json

from aiohttp import ClientSession
from typing import Dict

import coloredlogs

from tasks.utils.database import databases
from tasks.supplier_statics import Providers


DB = databases('agent')
HEADERS = {
    "accept-version": "5.0.0",
    "x-jwt-token": "599ad88aec48a951bbb7811c77208d74"
}

LOGGER = logging.getLogger(__name__)
level_style = {
    'debug': {'color': 'blue'},
    'info': {'color': 'white'},
    'warning': {'color': 'yellow'},
    'error': {'color': 'red'},
    'critical': {'bold': True, 'color': 'red'}
}
coloredlogs.install(
    level='DEBUG', isatty=True, level_styles=level_style,
    fmt='%(asctime)s %(name)s %(levelname)s %(message)s'
)


def supplier_table(supplier: str):
    return DB.get_collection(
        f'statics.hotels.{supplier}'
    )


async def fetch_chs(name: str,
                    meth: str = 'GET',
                    url: str = 'https://api.weegotr.com/api/google/translate',
                    headers: Dict = HEADERS
                    ) -> str:
    params = {
            'target': 'zh-CN',
            'q': name
        }
    try:
        async with ClientSession() as session:
            async with session.request(meth, url, params=params, headers=headers) as resp:
                text = await resp.text()
                status = resp.status
    except Exception:
        LOGGER.error('', exc_info=True)
        return
    if status != 200:
        LOGGER.error(
            f'Unexpected response: <%s> %s',
            status, text
        )
        return
    response = json.loads(text)

    '''
    response结构为
    {
        "data": {
            "translations": [
                {
                    "translatedText": "年龄",
                    "detectedSourceLanguage": "en"
                },
                {
                    "translatedText": "名称",
                    "detectedSourceLanguage": "en"
                }
            ]
        }
    }
    translations对应request参数中的q，每次请求一个单词，所以每次取translations中的第一个
    '''
    translations = response.get('data', {}).get('translations', [])
    if not translations:
        LOGGER.error('Empty translations: %s', translations)
        return
    translation = translations[0].get('translatedText')
    return translation


async def update_doc(doc: Dict) -> None:
    supplier_table(doc['supplier']).update_one(
        {
            '_id': doc['ori_id']
        },
        {
            "$set":
                {
                    'ctrip_name': doc['ctrip_name']
                }
        }
    )
    supplier_table("without_ctrip_name").delete_one({
        '_id': doc['_id']
    })


async def update_name_cn(doc):
    name_cn = await fetch_chs(doc['name'])
    if name_cn:
        doc['ctrip_name'] = name_cn
        try:
            await update_doc(doc)
            LOGGER.info(f'Update {doc} succeed.')
        except Exception as exc:
            LOGGER.error('%s: %s', exc, doc)
    else:
        LOGGER.warning(f'Fetch {doc} failed')


def main():

    # 创建包含所有缺少中文名的数据组成的新表
    # supplier_table('without_ctrip_name').drop()
    # for provider in Providers:
    #     _provider = provider.value
    #     for doc in supplier_table(_provider).find({'ctrip_name': {'$exists': False}}, no_cursor_timeout=True):
    #         supplier_table('without_ctrip_name').insert_one({
    #             'ori_id': doc['_id'],
    #             'name': doc['name'],
    #             'supplier': _provider
    #         })
    #     LOGGER.info(f'Insert docs from {_provider} finished')
    docs = supplier_table('without_ctrip_name').find({}, no_cursor_timeout=True)
    docs_num = docs.count()

    # 更新所有数据
    loop = asyncio.get_event_loop()
    for index, doc in enumerate(docs):
        loop.run_until_complete(asyncio.ensure_future(update_name_cn(doc)))
        progress = (index + 1) / docs_num * 100
        LOGGER.info('Progress: %.2f%%', progress)


if __name__ == '__main__':
    main()
