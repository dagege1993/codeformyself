# coding: utf-8
# Standard Library
import logging

# Third Party
import aiohttp
from web import settings
from bson import ObjectId
from sanic.response import json
from web.utils.database import databases
from web.utils.fix_statics_data import get_hotel_data

from . import api_v1
from .create_hotel import supplier_data
from .formatter_response import rest_result


@api_v1.route("/hotels/sim", methods=["GET"])
async def caculate(request):
    logger = logging.getLogger(__name__)
    hub = databases("hub")
    supplier_id = request.args.get("supplier")
    hotel_id = request.args.get("hotel_id")
    name_cms = request.args.get("name_cms", "").replace("undefined", "")
    addr_cms = request.args.get("addr_cms", "").replace("undefined", "")
    city_id = request.args.get("city_id", "").replace("undefined", "")
    latitude = request.args.get("latitude", "").replace("undefined", "")
    longitude = request.args.get("longitude", "").replace("undefined", "")
    logger.info(f"query args : {request.args}")
    try:
        city_name = await hub["meta_cities"].find_one(
            {"_id": ObjectId(city_id)}
        )
        city_name = city_name.get("name_en", " ")
    except Exception as exc:
        logger.error(f"invalid city id : {city_id}", exc_info=exc)
        city_name = " "
    datas = await supplier_data(supplier_id, hotel_id)
    if not datas:
        provider = settings.SUPPLIER_ID_2_NAME.get(supplier_id, supplier_id)
        if provider in ["hotelspro", "hotelbeds"]:
            fix_hotel = await get_hotel_data(provider, [hotel_id])
            if not fix_hotel:
                logger.error(f"{provider}: {hotel_id} statics data not find!")
                return json(
                    {
                        "status": 400,
                        "errmsg": "statics provider data not find",
                    },
                    status=200,
                )
            else:
                fix_hotel = fix_hotel[0]
                if not isinstance(fix_hotel, dict):
                    logger.error(
                        f"{provider}: {hotel_id} statics data not find!"
                    )
                    return json(
                        {
                            "status": 404,
                            "errmsg": "statics provider data not find",
                        },
                        status=200,
                    )
                datas["name_en"] = fix_hotel.get("name", "")
                datas["address"] = (
                    fix_hotel.get("address", "")
                    + fix_hotel.get("address1", "")
                    + fix_hotel.get("address2", "")
                )
                datas["longitude"] = fix_hotel.get("longitude", "")
                datas["latitude"] = fix_hotel.get("latitude", "")
        else:
            logger.error(f"{provider}: {hotel_id} statics data not find!")
            return json(
                {"status": 404, "errmsg": "statics provider data not find"},
                status=200,
            )
    if latitude and longitude and datas["latitude"] and datas["longitude"]:
        lng_error = abs(float(longitude) - float(datas["longitude"]))
        lat_error = abs(float(latitude) - float(datas["latitude"]))
        if (lng_error > 0.01) or (lat_error > 0.01):
            return rest_result(
                request,
                {
                    "status": 200,
                    "data": {
                        "prob": 0.5,
                        "hotel_name": datas.get("name_en", ""),
                        "hotel_addr": datas.get("address", ""),
                        "hotel_latitude": datas["latitude"],
                        "hotel_longitude": datas["longitude"],
                    },
                },
            )
    async with aiohttp.ClientSession() as sess:
        async with sess.get(
            f"{settings.EXAMINER_API}/api/v1/examiner/similarity",
            params={
                "city": city_name,
                "name_supplier": datas.get("name_en", "").lower(),
                "address_supplier": datas.get("address", "").lower(),
                "name_cms": name_cms.lower(),
                "address_cms": addr_cms.lower(),
            },
        ) as resp:
            resp = await resp.json()
    if not resp:
        logger.warning(f"hotel_id:{hotel_id} similarity return null")
        return rest_result(
            request, {"status": 400, "errmsg": "similarity return null!"}
        )
    elif resp.get("status") != 200:
        logger.warning(
            f'hotel_id:{hotel_id}' \
            f'something wrong with caculate similar\n{resp.get("errmsg", "")}'
        )
        return rest_result(
            request,
            {
                "status": 200,
                "data": {
                    "prob": 0.5,
                    "hotel_name": datas.get("name_en", ""),
                    "hotel_addr": datas.get("address", ""),
                },
                "errmsg": "something wrong with" \
                f" caculate similar\n{resp.get('errmsg', '')}",
            },
        )
    else:
        request.headers["accept"] = "application/json"
        return rest_result(
            request,
            {
                "status": 200,
                "data": {
                    "prob": resp["data"],
                    "hotel_name": datas.get("name_en", ""),
                    "hotel_addr": datas.get("address", ""),
                },
            },
        )
