# coding: utf-8

import logging
import typing
import asyncio
from bson import ObjectId
from sanic import exceptions, response
from functools import partial

from web.api import api_v1
from web.utils.database import databases


@api_v1.post("/hotels/relux/rooms")
async def update_hotel(request):
    logger = logging.getLogger(__name__)
    try:
        body = request.json
    except exceptions.InvalidUsage:
        body = None
    if not body or not isinstance(body, dict):
        logger.warning(
            f"Invalid request body: {request.body}"
        )
        raise exceptions.InvalidUsage(
            {
                "status": 400,
                "errmsg": "Invalid request body"
            }
        )

    oid = body.get("_id")
    if not oid:
        logger.warning('_id is required!')
        raise exceptions.InvalidUsage(
            {
                "status": 400,
                "errmsg": "_id is required!"
            }
        )
    db = databases("scripture")
    doc = await db.statics.hotels.relux.rooms.find_one(
        {"_id": ObjectId(oid)},
        {"rooms_cn": 1}
    )
    if not doc:
        logger.warning(f'oid:{oid} Corresponding Hotel not found')
        raise exceptions.NotFound(
            {
                "status": 404,
                "errmsg": "Hotel not found!"
            }
        )
    ori_rooms_cn = doc.get("rooms_cn")
    if not ori_rooms_cn:
        logger.warning(f'oid:{oid} Corresponding Hotel rooms_cn not found')
        raise exceptions.NotFound(
            {
                "status": 404,
                "errmsg": "Hotel rooms_cn not found!"
            }
        )
    rooms_cn = body.get("rooms_cn")
    if not rooms_cn:
        logger.warning(f'oid:{oid} Corresponding rooms_cn is required')
        raise exceptions.InvalidUsage(
            {
                "status": 400,
                "errmsg": "rooms_cn is required!"
            }
        )

    futures = []
    for room, ori_room in zip(rooms_cn, ori_rooms_cn):
        room_id = room["id"]
        if room_id != ori_room["id"]:
            logger.error(
                f"The order of the rooms is out of order: "
                f"room({room}), ori_doc({doc})")
            continue
        if room == ori_room:
            continue

        for plan, ori_plan in zip(
                room.get("plans", []), ori_room.get("plans", [])
        ):
            if plan["id"] != ori_plan["id"]:
                logger.error(
                    f"The order of the plans is out of order: "
                    f"plan({plan}), ori doc({doc})")
                continue
            if plan == ori_plan:
                continue
            if plan["name"] != ori_plan["name"]:
                plan["ori_name"] = ori_plan["name"]
            if plan["feature"] != ori_plan["feature"]:
                plan["ori_feature"] = ori_plan["feature"]
        future = asyncio.ensure_future(
            db.statics.hotels.relux.rooms.update_one(
                {
                    "_id": ObjectId(oid),
                    "rooms_cn.id": room_id,
                    "rooms_cn.plans": ori_room["plans"]
                },
                {"$set": {"rooms_cn.$.plans": room["plans"]}}
            )
        )
        extra = {
            "oid": oid,
            "ori_plan": ori_room["plans"],
            "new_plan": room["plans"]
        }
        future.add_done_callback(partial(callback, extra=extra))
        futures.append(future)

    if not futures:
        logger.warning(f'ori_room["plans"]:{ori_room["plans"]},room["plans"]:{room["plans"]},'
                       f' No difference or rooms order is wrong')
        raise exceptions.InvalidUsage(
            {
                "status": 400,
                "errmsg": "No difference or rooms order is wrong"
            }
        )
    logger.info(f'oid:{oid} update_relux_plan success')
    return response.json({"status": 200, "data": {"count": len(futures)}})


def callback(future: asyncio.Future, extra: typing.Dict):
    logger = logging.getLogger(
        f"{__name__}.update_relux_plan.callback")
    if future.exception():
        logger.error(f"Update plan failed: \nextra({extra})",
                     exc_info=future.exception(), extra=extra)
    res = future.result()
    if res.modified_count != 1:
        logger.error(f"Update plan failed:\n raw_result({res.raw_result})\n, extra({extra})", extra=extra)
