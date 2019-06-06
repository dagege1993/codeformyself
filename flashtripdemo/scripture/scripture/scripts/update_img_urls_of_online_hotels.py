# coding: utf-8

import os
import asyncio
import typing
import logging
from bson import ObjectId
from functools import partial

import aiohttp
import coloredlogs

from web.utils.database import databases

level_style = {
    'debug': {'color': 'blue'},
    'info': {'color': 'white'},
    'warning': {'color': 'yellow'},
    'error': {'color': 'red'},
    'critical': {'bold': True, 'color': 'red'}
}
coloredlogs.install(
    level='INFO', isatty=True, level_styles=level_style,
    fmt='%(asctime)s %(name)s %(levelname)s %(message)s'
)


async def fetch_links(facilities: typing.List[typing.Dict]) -> typing.List:
    if os.environ.get('IS_PRODUCTION'):
        endpoint = 'https://scripture.weegotr.com'
    else:
        endpoint = 'http://0.0.0.0:4010'
    url = f'{endpoint}/api/v1/facilities'
    headers = {'Accept': 'application/json'}
    payload = {"facilities": facilities}
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload, headers=headers) as resp:
            text = await resp.text()
            assert resp.status == 200, text
            json = await resp.json()
            assert json.get('status') == 200, text
            return json.get("data")


def ensure_json(obj: typing.Any) -> typing.Any:
    if isinstance(obj, list):
        return [ensure_json(o) for o in obj]
    if isinstance(obj, dict):
        return {key: ensure_json(val) for key, val in obj.items()}
    if isinstance(obj, ObjectId):
        return str(obj)
    if isinstance(obj, (str, int, float, bool)):
        return obj
    if obj is None:
        return obj
    raise ValueError(f'Unknown type: {obj}, typo({type(obj)})')


def ensure_bson(documents: typing.List[typing.Dict],
                mapping: typing.Dict) -> typing.List:
    for document in documents:
        for key, func in mapping.items():
            if key in document:
                document[key] = func(document[key])
    return documents


def callback(future, oid):
    logger = logging.getLogger(f"{__name__}.callback")
    if future.exception():
        logger.error(f"Update failed: {oid}",
                     exc_info=future.exception())
    res = future.result()
    if res.modified_count != 1:
        if res.raw_result.get('updatedExisting'):
            logger.warning(f"updatedExisting: {oid}, {res.raw_result}")
        else:
            logger.error(f"Update failed: {oid}, {res.raw_result}")


async def update() -> None:
    logger = logging.getLogger(f'{__name__}.update')
    db = databases("hub")
    query = {
        "__t": "Hotel",
        "edit_status": {
            "$in": ["edited", "audited"]
        },
        "publish_status": "online"
    }
    count = await db.poi_items.count_documents(query)
    progress = 0

    async for doc in db.poi_items.find(query, {'facilities': 1}):
        logger.info('progress: {:.2%}'.format(progress/count))
        progress += 1
        facilities = doc.get('facilities')
        if not facilities:
            logger.warning(f'No facilities: {doc["_id"]}')
            continue
        try:
            facilities = ensure_json(facilities)
        except ValueError as exc:
            logger.error(f'{exc}\n _id: {doc["_id"]}')
            continue
        except Exception as exc:
            logger.critical(f'Unknown_error, _id: {doc["_id"]}',
                            exc_info=exc)
            continue
        try:
            data = await fetch_links(facilities)
        except AssertionError as exc:
            logger.error(f'Status unexpected: {exc}, _id: {doc["_id"]}')
            continue
        except Exception as exc:
            logger.critical(f'Unknown_error, _id: {doc["_id"]}',
                            exc_info=exc)
            continue
        try:
            updated_facilities = ensure_bson(data, {"_id": ObjectId})
        except Exception as exc:
            logger.critical(f'Unknown_error, _id: {doc["_id"]}',
                            exc_info=exc)
            continue
        future = asyncio.ensure_future(
            db.poi_items.update_one(
                {'_id': doc['_id']}, {'$set': {'facilities': updated_facilities}})
        )
        future.add_done_callback(partial(callback, oid=doc["_id"]))


def main():
    asyncio.get_event_loop().run_until_complete(update())


if __name__ == "__main__":
    main()
