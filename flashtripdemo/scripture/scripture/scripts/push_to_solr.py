# coding: utf8

# Standard Library
import json
import time
from functools import lru_cache

# First Party
import yaml
import pinyin
from pysolr import Solr
from pymongo import MongoClient
from tasks.utils.database import databases
from bson import ObjectId

# Current Project
import requests

# from solrcloudpy import SolrConnection


db = databases("agent")
hub_db = databases("hub")

solr_host = "172.16.1.223"

def push_hotels(cursor, supplier):
    solr = Solr(f"http://{solr_host}/solr/hotels")
    docs = []
    index = 1
    total = cursor.count()
    for doc in cursor:
        d = {
            "id": str(doc["_id"]),
            "name": doc["name"],
            "name_cn": doc.get("name_cn", ""),
            "supplier": supplier,
            "address": doc["address"],
            "wgstar": doc["wgstar"],
        }

        if "city" in doc:
            d["city"] = doc["city"].get("name", "")
        if "country" in doc:
            country_name = (doc["country"].get("name", ""),)
            country_code = doc["country"].get("code", "")
            if "name" in doc["country"]:
                d["country"] = country_name
            else:
                d["country"] = country_code
        weego_id = doc.get("weego_id")
        if weego_id:
            d["to_c_ref"] = str(weego_id)
        wg_country_id = doc.get("wg_country_id")
        if wg_country_id:
            d["wg_country_id"] = str(wg_country_id)
        wg_province_id = doc.get("wg_province_id")
        if wg_province_id:
            d["wg_province_id"] = str(wg_province_id)
        wg_city_id = doc.get("wg_city_id")
        if wg_city_id:
            d["wg_city_id"] = wg_city_id
        wg_destination_id = doc.get("wg_destination_id")
        if wg_destination_id:
            d["wg_destination_id"] = wg_destination_id
        docs.append(d)
        if index % 500 == 0:
            try:
                print(solr.add(docs, commit=True))
                docs.clear()
                print(
                    "Progress of {1}: {0:.2f}%".format(
                        index / total * 100, supplier
                    )
                )
            except Exception as e:
                print("------------------------------------------------------")
                print(index)
                print("------------------------------------------------------")
                raise
        index += 1

    if docs:
        print(solr.add(docs, commit=True))
        print(index)
        print(
            "Progress of {1}: {0:.2f}%".format(index / total * 100, supplier)
        )


def update_all_hotels(*, drop=False):
    if drop:
        solr_drop("hotels")

    projection = {
        "_id": 1,
        "name": 1,
        "name_cn": 1,
        "city.name": 1,
        "country.name": 1,
        "address": 1,
        "wgstar": 1,
        "weego_id": 1,  # weego to c id
        "wg_country_id": 1,
        "wg_province_id": 1,
        "wg_city_id": 1,
        "wg_destination_id": 1,
    }

    with open("data/countries.yml") as yml:
        countries = yaml.load(yml)
    for provider in ["bonotel", "jactravel", "hotelspro"]:
        cursor = db.statics.hotels[provider].find(
            {
                "country.name": {"$in": list(countries[provider].keys())},
                "wgstar": {"$gte": 3},
            },
            projection,
            no_cursor_timeout=True,
        )
        push_hotels(cursor, provider)

    projection.pop("country.name")
    projection["country.code"] = 1
    hb = db.statics.hotels.hotelbeds.find(
        {
            "country.code": {"$in": list(countries["hotelbeds"].keys())},
            "wgstar": {"$gte": 3},
        },
        projection,
        no_cursor_timeout=True,
    )
    push_hotels(hb, "hotelbeds")

    whotel = db.statics.hotels.whotel.find(
        {"wgstar": {"$gte": 3}}, projection, no_cursor_timeout=True
    )
    push_hotels(whotel, "whotel")


@lru_cache(256)
def get_country_by_id(country_id):
    return db.statics.countries.find_one(
        {"_id": country_id}, {"name_cn": 1, "name_en": 1, "name_alts": 1}
    )


@lru_cache(1024)
def get_province_by_id(province_id):
    return db.statics.provinces.find_one(
        {"_id": province_id}, {"name_cn": 1, "name_en": 1, "name_alts": 1}
    )


@lru_cache(2048)
def get_city_by_id(city_id):
    return db.statics.cities.find_one(
        {"_id": city_id}, {"name_cn": 1, "name_en": 1, "name_alts": 1}
    )


def push_destinations(destination_table):
    docs = []
    index = 0
    type_mapping = {
        "destinations": {"type_name": "destination", "type_code": 8},
        "cities": {"type_name": "city", "type_code": 16},
        "provinces": {"type_name": "province", "type_code": 32},
        "countries": {"type_name": "country", "type_code": 64},
    }
    destinations = db.statics[destination_table].find(
        {},
        {
            "country_id": 1,
            "province_id": 1,
            "city_id": 1,
            "name_cn": 1,
            "name_en": 1,
            "name_alts": 1,
            "weight": 1,
            "hotel_count": 1,
        },
        no_cursor_timeout=True,
    )
    total = destinations.count()
    for destination in destinations:
        doc = {
            "name_en": destination["name_en"],
            "name_cn": destination.get("name_cn", ""),
            "type": type_mapping[destination_table]["type_name"],
            "type_code": type_mapping[destination_table]["type_code"],
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
            country = get_country_by_id(country_id)
            if not country:
                country = {"name_cn": "", "name_en": ""}
            doc["country_id"] = str(country_id)
            doc["country_name_cn"] = country.get("name_cn", "")
            doc["country_name_en"] = country["name_en"]
        if province_id:
            province = get_province_by_id(province_id)
            if not province:
                province = {"name_cn": "", "name_en": ""}
            doc["province_id"] = str(province_id)
            doc["province_name_cn"] = province.get("name_cn", "")
            doc["province_name_en"] = province["name_en"]
        if city_id:
            city = get_city_by_id(city_id)
            if not city:
                city = {"name_cn": "", "name_en": ""}
            doc["city_id"] = str(city_id)
            doc["city_name_cn"] = city.get("name_cn", "")
            doc["city_name_en"] = city["name_en"]

        docs.append(doc)
        index += 1
        if (index % 500) == 0:
            try:
                solr_add(docs)
                docs.clear()
                print(
                    "Progress of {1}: {0:.2f}%".format(
                        index / total * 100, destination_table
                    )
                )
            except Exception as e:
                print("------------------------------------------------------")
                print(index)
                print("------------------------------------------------------")
                raise

    if docs:
        solr_add(docs)
        docs.clear()
        print(index)
        print(
            "Progress of {1}: {0:.2f}%".format(
                index / total * 100, destination_table
            )
        )

def get_hub_products_query_condition(product_type, ids=None):
    projection = {"_id": 1, "name": 1, "name_en": 1, "is_recommend": 1, "city": 1}
    if product_type == "hotels":
        condition = {
            "__t": "Hotel",
            "edit_status": {"$in": ["edited", "audited"]},
            "publish_status": "online",
        }
    elif product_type == "packages":
        condition = {
            "edit_status": {"$in": ["edited", "audited"]},
            "publish_status": "online",
        }
    else:
        condition = {}
        projection = {
            "_id": 1,
            "name": 1,
            "name_en": 1,
            "name_py": 1,
            "code": 1,
            "latitude": 1,
            "longitude": 1,
            "cover_image_url": 1,
            "app_image_url": 1,
            "service_telephone": 1,
            "country": 1,
            "is_hot": 1,
            "is_open": 1,
            "is_show_in_city_home": 1,
            "is_recommend_hotel": 1,
            "is_recommend_package": 1,
            "has_product": 1,
            "has_package": 1,
            "categories.attractions": 1,
            "categories.restaurants": 1,
            "categories.shoppings": 1,
            "categories.products": 1,
            "categories.hotels": 1,
        }

    if ids:
        if isinstance(ids, str):
            ids = [ids]

        ids = list(map(lambda x: ObjectId(x), ids))
        condition["_id"] = {
            "$in": ids
        }

    return condition, projection

def get_hub_products_solr_data(product_type, products):
    """
    add hub products: hotels or packages or cities to solr
    """

    if not products:
        return

    docs = []
    for product in products:
        doc = {
            "id": str(product["_id"]),
            "type": product_type,
            "name": product["name"],
            "name_py": pinyin.get(product["name"], format="strip"),
            "name_en": str(product.get("name_en", "")),
            "is_recommend": str(product.get("is_recommend", False)),
        }

        if product_type == "city":
            if "country" in product:
                country = hub_db["meta_countries"].find_one( {"_id": product["country"]},
                    {"name": 1, "name_en": 1, "code": 1, "continent": 1},
                )
                country["_id"] = str(country["_id"])
                doc["country"] = json.dumps(country)

            if "categories" in product:
                categories = hub_db["meta_categories"].find_one(
                    {"_id": product["categories"]},
                    {
                        "categories.attractions.name": 1,
                        "categories.attractions.name_en": 1,
                        "categories.restaurants.name": 1,
                        "categories.restaurants.name_en": 1,
                        "categories.shoppings.name": 1,
                        "categories.shoppings.name_en": 1,
                        "categories.products.name": 1,
                        "categories.products.name_en": 1,
                        "categories.hotels.name": 1,
                        "categories.hotels.name_en": 1,
                    },
                )

            doc["service_telephone"] = json.dumps(product["service_telephone"])
            doc["name_py"] = product["name_py"]
            doc["code"] = product.get("code", "")
            doc["latitude"] = product.get("latitude", None)
            doc["longitude"] = product.get("longitude", None)
            doc["cover_image_url"] = product["cover_image_url"]
            doc["app_image_url"] = product["app_image_url"]
            doc["is_hot"] = product.get("is_hot", False)
            doc["is_open"] = product["is_open"]
            doc["is_show_in_city_home"] = product.get(
                "is_show_in_city_home", False
            )
            doc["is_recommend_hotel"] = product.get(
                "is_recommend_hotel", False
            )
            doc["is_recommend_package"] = product.get(
                "is_recommend_package", False
            )
            doc["has_product"] = product.get("has_product", False)
            doc["has_package"] = product.get("has_package", False)
        docs.append(doc)

    return docs

def _get_hub_products(product_type):
    try:
        type_mapping = {
            "hotels": "poi_items",
            "packages": "sku_packages",
            "city": "meta_cities",
        }
        condition, projection = get_hub_products_query_condition(product_type)

        products = list(hub_db[type_mapping[product_type]].find(
            condition, projection
        ))

        solr_docs = get_hub_products_solr_data(product_type, products)
        return solr_docs, products
    except Exception as e:
        print(e)

def _get_cities(city_ids):
    try:
        _, projection = get_hub_products_query_condition('city')
        products = hub_db['meta_cities'].find({'_id': {"$in": city_ids}}, projection)

        solr_docs = get_hub_products_solr_data('city', products)
        return solr_docs
    except Exception as e:
        print(e) 


def solr_add(docs, collection="destinations"):
    solr_endpoint = f"http://{solr_host}/solr/{collection}"
    jsondocs = json.dumps(docs, ensure_ascii=0).encode("utf8")
    resp = requests.post(
        "/".join([solr_endpoint, "update"]),
        params={"wt": "json", "commit": "true"},
        data=jsondocs,
        headers={"Content-Type": "application/json"},
    )
    assert resp.status_code == 200, resp.text
    print(resp.json())


def solr_drop(collection="destinations"):
    print(f"Collection({collection}) will be dropped.")
    return solr_add({"delete": {"query": "*:*"}}, collection=collection)


def update_all_destinations(*, drop=False):
    if drop:
        solr_drop("destinations")
    for dest_table in ["destinations", "cities", "provinces", "countries"]:
        push_destinations(dest_table)


def update_hub_products():
    try:
        hotel_solr_docs, hotels = _get_hub_products('hotels')
        package_solr_docs, packages = _get_hub_products('packages')

        hotel_city_ids = {item.get('city') for item in hotels}
        package_city_ids = {item.get('city') for item in packages}

        cities = list(hotel_city_ids) + list(package_city_ids)
        city_solr_docs = _get_cities(cities)

        print(f'hotel count: {len(hotels)}')
        print(f'package count: {len(packages)}')
        print(f'cities count: {len(cities)}')

        solr = Solr(f"http://{solr_host}/solr/hub-products")
        solr_drop('hub-products')
        solr.add(hotel_solr_docs + package_solr_docs + city_solr_docs)
        solr_res = solr.commit()
        print(f'SOLR UPDATE RESULT:')
        print(solr_res)
        print('SOLR INDEX UPDATE SUCCESS!')
    except expression as e:
        print('SOLR INDEX UPDATE FAILED!')
        print(e)


class Fire:
    def __init__(self, env="sandbox", drop=False):
        global db
        global hub_db
        global solr_host

        self._drop = False

        if env == "online":
            print("Warnning: updating online solr.")
            if drop:
                print("--drop 对线上环境不生效.")

            time.sleep(1)
        # if env == 'sandbox':
        #     solr_host = '172.16.4.110:8983'
        else:
            db = MongoClient("mongodb://172.16.4.110:27017").scripture
            hub_db = MongoClient("mongodb://172.16.4.110:27017").hub
            solr_host = "172.16.4.110:8983"
            if drop:
                self._drop = True
        self.env = env

    def destinations(self):
        update_all_destinations(drop=self._drop)

    def hotels(self):
        update_all_hotels(drop=self._drop)

    def hub_products(self):
        update_hub_products()


if __name__ == "__main__":
    import fire

    fire.Fire(Fire)
