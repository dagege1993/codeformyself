# coding: utf8

# Standard Library
import asyncio
import logging

# Non Standard Library
from sanic import Blueprint
from sanic.response import json

from web import settings
from bson import ObjectId
from pysolr import Solr
from web.utils.database import databases
from scripture.scripts.push_to_solr import get_hub_products_query_condition, get_hub_products_solr_data

solr_bp = Blueprint("solr", url_prefix="/api/v1/solr")

@solr_bp.post("/trigger/<collection_name>")
async def post_trigger(request, collection_name):
    try:
        logger = logging.getLogger("web.solr.post.trigger")
        logger.info("request body %s", request.json)

        if not request.json:
            return json({ "message": "invalid request body" }, status=400)

        handler = trigger_update_handler_map.get(collection_name, None)
        if not handler:
            logger.warning("invalid handler")
            return json({ "message": "invalid handler" }, status=400)

        res = await handler(request.json)
        return json({ "message": "success" })
    except Exception as e:
        logger.error("post trigger error, body: %s", request.json, exc_info=e)
        return json({ "message": str(e) }, status=400)

@solr_bp.delete("/trigger/<collection_name>")
async def delete_trigger(request, collection_name):
    try:
        logger = logging.getLogger("web.solr.delete.trigger")
        logger.debug("request body %s", request.json)

        handler = trigger_delete_handler_map.get(collection_name, None)
        if not handler:
            logger.warning("invalid handler")
            return json({ "message": "invalid handler" }, status=400)

        await handler(request.json)
        return json({ "message": "success" })
    except Exception as e:
        logger.error("post trigger error, body: %s", request.json, exc_info=e)
        return json({ "message": str(e) }, status=500)

@solr_bp.get("/trigger")
async def trigger(request):
    logger = logging.getLogger("web.solr.trigger")
    args = request.args
    logger.debug("Got request %s", args)
    destinations = args.getlist("destinations")
    provinces = args.getlist("provinces")
    cities = args.getlist("cities")
    hotels = args.getlist("hotels")

    if hotels:
        logger.debug("Update hotels in solr. %s", await hotel(hotels))
    if cities:
        logger.debug(
            "Update cities in solr. %s", await destination(cities, "cities")
        )
    if destinations:
        logger.debug(
            "Update destinations in solr. %s", await destination(destinations)
        )
    if provinces:
        logger.debug(
            "Update provinces in solr. %s",
            await destination(provinces, "provinces"),
        )

    return json(
        {
            "destinations": destinations,
            "provinces": provinces,
            "cities": cities,
            "hotels": hotels,
        }
    )


async def hotel(hotel_ids):
    hotel_mapping = {}
    for item in hotel_ids:
        provider, _id = item.split(":")
        hotel_mapping.setdefault(provider, []).append(ObjectId(_id))
    docs = []
    for provider, ids in hotel_mapping.items():
        async for hotel in (
            databases("agent")
            .get_collection(provider)
            .find({"_id": {"$in": ids}})
        ):
            docs.append(HotelDoc(hotel, provider))
    return await solr_add(docs, "hotels")


async def solr_add(docs, collection):
    return await (
        asyncio.get_event_loop().run_in_executor(
            None, _solr_add, docs, collection
        )
    )

async def solr_del(ids, collection):
    return await (
        asyncio.get_event_loop().run_in_executor(
            None, _solr_del, collection, ids
        )
    )

def _solr_add(docs, collection):
    solr = Solr(
        "/".join([settings.SOLR.rstrip("/"), "solr", collection])
    )
    return solr.add(docs, commit=True)

def _solr_del(collection, ids):
    solr = Solr(
        "/".join([settings.SOLR.rstrip("/"), "solr", collection])
    )
    return solr.delete(id=ids, commit=True)

def HotelDoc(hotel, provider):
    doc = {
        "id": str(hotel["_id"]),
        "name": hotel["name"],
        "name_cn": hotel.get("name_cn", ""),
        "supplier": provider.split(".")[-1],
        "address": hotel["address"],
        "wgstar": hotel["wgstar"],
    }
    if "city" in hotel:
        doc["city"]: hotel["city"].get("name", "")
    if "country" in doc:
        country_name = (hotel["country"].get("name", ""),)
        country_code = hotel["country"].get("code", "")
        if "name" in hotel["country"]:
            doc["country"] = country_name
        else:
            doc["country"] = country_code
    weego_id = hotel.get("weego_id")
    if weego_id:
        doc["to_c_ref"] = str(weego_id)
    wg_country_id = hotel.get("wg_country_id")
    if wg_country_id:
        doc["wg_country_id"] = str(wg_country_id)
    wg_province_id = hotel.get("wg_province_id")
    if wg_province_id:
        doc["wg_province_id"] = str(wg_province_id)
    wg_city_id = hotel.get("wg_city_id")
    if wg_city_id:
        doc["wg_city_id"] = wg_city_id
    wg_destination_id = hotel.get("wg_destination_id")
    if wg_destination_id:
        doc["wg_destination_id"] = wg_destination_id
    return doc


async def destination(destnation_ids, type_name="destinations"):
    type_mapping = {
        "destinations": {"type_name": "destination", "type_code": 8},
        "cities": {"type_name": "city", "type_code": 16},
        "provinces": {"type_name": "province", "type_code": 32},
        "countries": {"type_name": "country", "type_code": 64},
    }
    docs = []
    awaitable_cursor = (
        databases("agent")
        .get_collection("statics.{}".format(type_name))
        .find(
            {"_id": {"$in": [ObjectId(_id) for _id in destnation_ids]}},
            {
                "country_id": 1,
                "province_id": 1,
                "city_id": 1,
                "name_cn": 1,
                "name_en": 1,
                "name_alts": 1,
                "weight": 1,
            },
        )
    )
    async for destination in awaitable_cursor:
        doc = {
            "name_en": destination["name_en"],
            "name_cn": destination.get("name_cn", ""),
            "type": type_mapping[type_name]["type_name"],
            "type_code": type_mapping[type_name]["type_code"],
            "id": str(destination["_id"]),
            "weight": destination["weight"],
            "hotel_count": destination.get("hotel_count", 0),
        }

        if "name_alts" in destination:
            name_alts = destination["name_alts"].split(",")
        else:
            name_alts = []
            if doc["name_en"]:
                name_alts.append(doc["name_en"])
            if doc["name_cn"]:
                name_alts.append(doc["name_cn"])
        doc["name_alts"] = name_alts
        country_id = destination.get("country_id")
        province_id = destination.get("province_id")
        city_id = destination.get("city_id")
        if country_id:
            country = await get_country_by_id(country_id) or {
                "name_cn": "",
                "name_en": "",
            }
            # doc["country_id"] = str(country_id)
            doc["country_name_cn"] = country.get("name_cn", "")
            doc["country_name_en"] = country["name_en"]
        if province_id:
            province = await get_province_by_id(province_id) or {
                "name_cn": "",
                "name_en": "",
            }
            # doc["province_id"] = str(province_id)
            doc["province_name_cn"] = province.get("name_cn", "")
            doc["province_name_en"] = province["name_en"]
        if city_id:
            city = await get_city_by_id(city_id) or {
                "name_cn": "",
                "name_en": "",
            }
            # doc["city_id"] = str(city_id)
            doc["city_name_cn"] = city.get("name_cn", "")
            doc["city_name_en"] = city["name_en"]
        docs.append(doc)
    return await solr_add(docs, "destinations")


async def get_country_by_id(country_id):
    return await databases("agent").statics.countries.find_one(
        {"_id": country_id}, {"name_cn": 1, "name_en": 1, "name_alts": 1}
    )


async def get_province_by_id(province_id):
    return await databases("agent").statics.provinces.find_one(
        {"_id": province_id}, {"name_cn": 1, "name_en": 1, "name_alts": 1}
    )


async def get_city_by_id(city_id):
    return await databases("agent").statics.cities.find_one(
        {"_id": city_id}, {"name_cn": 1, "name_en": 1, "name_alts": 1}
    )

async def upsert_hub_products(data):
    if (
        not data
        or ("product_type" not in data)
        or ("id" not in data)
    ):
        raise Exception("invalid data")

    product_type = data["product_type"]
    product_ids = data["id"]

    condition, projection = get_hub_products_query_condition(product_type, product_ids)

    type_mapping = {
        "hotels": "poi_items",
        "packages": "sku_packages",
        "city": "meta_cities",
    }

    products = await databases("hub")[type_mapping[product_type]].find(
        condition, projection
    ).to_list(length=None)

    docs = get_hub_products_solr_data(product_type, products)

    if not docs:
        raise Exception("no docs udpated")

    return await solr_add(docs, 'hub-products')

async def delete_hub_products(data):
    if not data or "id" not in data:
        raise Exception("invalid data")

    ids = data["id"]
    if isinstance(ids, str):
        ids = [ids]

    return await solr_del(ids, 'hub-products')

trigger_update_handler_map = {
    "hub-products": upsert_hub_products
}

trigger_delete_handler_map = {
    "hub-products": delete_hub_products
}
