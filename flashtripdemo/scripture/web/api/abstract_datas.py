# coding: utf-8
import json
import logging
import re
from functools import reduce

import requests
from bson import ObjectId
from lxml import etree
from w3lib.html import remove_tags
from yarl import URL

from scripture.xpath import hotels as hotels_xp
from scripture.xpath import bookings_v2 as hotels_bk
from web.utils.database import databases
from scripture.models.hub_hotel import executor, transfor_pic_url
from web import settings

useless_facilities = ["咖啡美味！", "不允许携带宠物入住。", "水果", "（额外付费）", "宠物", "免费！"]
relux_room_type_word = settings.RELUX_FORBIDDEN_ROOM_TYPE_WORD


async def crawl_booking(cid, url):
    logger = logging.getLogger(__name__)
    scripture = databases("scripture")
    statics_data = await scripture["capture_urls"].find_one(
        {"_id": ObjectId(cid)}
    )
    quoter = statics_data.get("quoter")
    hid = statics_data.get("hid")
    payload = paras_booking_payload(url)
    if quoter and hid:
        where_clouser = {"quoter": quoter, "hid": hid}
        bookings_id = f"{quoter}::{hid}"
    else:
        where_clouser = {"capture_urls_id": cid}
        bookings_id = cid
        payload["capture_urls_id"] = cid
    res = await scripture.bookings.update_one(
        where_clouser, {"$set": payload}, upsert=True
    )
    if res:
        await scripture.capture_urls.update_one(
            {"_id": statics_data["_id"]},
            {
                "$set": {
                    "_hotels_cn_id": statics_data.get("hotels_cn_id"),
                    "hotels_cn_id": "",
                    "bookings_id": bookings_id,
                    "jset_id": "",
                    "_jset_id": statics_data.get("jset_id"),
                }
            },
        )
        logger.info(f'cid:{cid},url:{url},update statics data success')
        return {"status": 200, "data": payload}
    else:
        logger.error(f'cid:{cid},url:{url},update statics data faild')
        return {"status": 500, "errmsg": f"update statics data faild!"}


def paras_booking_payload(url):
    logger = logging.getLogger(__name__)
    payload = {}
    _url = URL(url)
    url = f"{_url.scheme}://{_url.host}{_url.path}"
    req = requests.get(url)
    req = req.content.decode("utf-8")
    et = etree.HTML(req)
    polices = find_polices(et)
    city_name = re.findall("city_name: '(.*?)'", req)
    latitude = re.findall("booking.env.b_map_center_latitude = (.*?);", req)
    longitude = re.findall("booking.env.b_map_center_longitude = (.*?);", req)
    ori_hotel_name = et.xpath(hotels_bk.ORI_HOTEL_NAME)[0].strip().split('（')
    if len(ori_hotel_name) == 1:
        hotel_name = hotel_name_en = ori_hotel_name[0]
    else:
        hotel_name, hotel_name_en = ori_hotel_name[1][:-1], ori_hotel_name[0]
    hotel_address = remove_line_break(et.xpath(hotels_bk.HOTEL_ADDRESS))
    facilities = [
        {"facility": name.strip()}
        for name in set(
            remove_line_break(
                et.xpath(hotels_bk.FACILITIES)[0].xpath(
                    "string(.)"
                )
            ).split("\n")
        )
        if name not in useless_facilities
    ]
    main_facilities = [
        {"facility": name.strip()}
        for name in set(et.xpath(hotels_bk.MAIN_FACILITIES))
        if name.strip() != ""
    ]
    restaurant_nums = re.findall("内设\d+家餐厅", req)
    if restaurant_nums:
        restaurant_nums = restaurant_nums[0]
        main_facilities.append({"facility": restaurant_nums})
    introduction = remove_line_break(
        et.xpath('//div[@id="summary"]')[0].xpath("string(.)")
    ).replace("位置超赞\n-\n查看地图\n", "")
    attractions = [
        {
            "name": remove_line_break(landmark.xpath("string(.)")).split("\n")[
                0
            ],
            "distance": remove_line_break(landmark.xpath("string(.)"))
            .split("\n")[-1]
            .replace("km", "公里"),
        }
        for landmark in et.xpath(hotels_bk.LANDMARKS)
    ]
    gallery = [
        {"image_url": ori_url}
        for ori_url in re.findall("highres_url: '(.*?)'", req)
    ]
    rooms = []
    rooms_base_node = et.xpath(hotels_bk.ROOMS_BASE_NODE)
    if rooms_base_node:
        rooms_base_node = rooms_base_node[0]
        info_pages = rooms_base_node.xpath(hotels_bk.INFO_PAGES)
        order_pages = rooms_base_node.xpath(hotels_bk.ORDER_PAGES)
    else:
        logger.warning(f"this booking.com page not find rooms! {url}")
        info_pages = []
        order_pages = []
    
    names_en = et.xpath(hotels_bk.NAMES_EN)
    names_cn = [
        name.strip()
        for name in et.xpath(hotels_bk.NAMES_CN)
        if name.strip() != ""
    ]
    for i in range(len(info_pages)):
        room = {}
        info_node = info_pages[i]
        order_node = order_pages[i]
        room["bed_size"] = ""
        room["add_bed_type"] = []
        room["useful"] = ""
        room["serve"] = ""
        room["network"] = ""
        room["recreation"] = ""
        room["dining"] = ""
        room["room_type_en"] = names_en[i].strip()
        room["room_type"] = names_cn[i]

        room["gallery"] = [
            {"image_url": url}
            for url in info_node.xpath(hotels_bk.ROOM_IMAGE)
        ]
        room["room_size"] = " ".join(
            [
                info.strip()
                for info in info_node.xpath(hotels_bk.ROOM_SIZE)
                if info.strip() != ""
            ]
        )
        if order_node.xpath(hotels_bk.ROOM_OCCUPANCY_INFO):
            room["occupancy_info"] = order_node.xpath(
                hotels_bk.ROOM_OCCUPANCY_INFO
            )[0].strip()
        else:
            room["occupancy_info"] = ""
        if order_node.xpath(hotels_bk.ROOM_BED_TYPE):
            room["bed_type"] = remove_line_break(
                order_node.xpath(hotels_bk.ROOM_BED_TYPE)[
                    0
                ].xpath("string(.)")
            )
        else:
            room["bed_type"] = ""
        ori_room_desc = "".join(info_node.xpath(hotels_bk.ROOM_DESC))
        room["room_desc"] = (
            remove_line_break(
                re.sub("我们网站上仅剩\d+间空房！", "", ori_room_desc)
                .replace("刚刚有人订过", "")
                .replace("选择床型：", "可选床型：")
                .replace("•", "")
            )
            .replace("\n和\n", "和")
            .replace("\n和\n", "和")
            .replace("-\n", "")
            .replace("\n平方米", "平方米")
            .split("其他设施包括")[0]
        )
        room["facilities"] = [
            {"facility": detail.replace("• ", "").strip()}
            for detail in info_node.xpath(
                hotels_bk.ROOM_FACILITIES
            )
        ]
        rooms.append(room)
    logging.debug(f"rooms : {len(rooms)}")
    payload["rooms"] = rooms
    payload["introduction"] = introduction
    payload["polices"] = polices
    payload["attractions"] = attractions
    payload["facilities"] = main_facilities
    payload["all_facilities"] = facilities
    payload["gallery"] = gallery
    if city_name:
        payload["city_name"] = city_name
    if latitude:
        payload["latitude"] = latitude[0]
    if longitude:
        payload["longitude"] = longitude[0]
    payload["name"] = hotel_name
    payload["name_en"] = hotel_name_en
    payload["address"] = hotel_address
    payload["bk_url"] = url
    return payload


async def crawl_hcom(capture_id, url):
    logger = logging.getLogger(__name__)
    scripture = databases("scripture")
    if len(capture_id) == 24:
        crawled = await scripture.capture_urls.find_one(
            {"_id": ObjectId(capture_id)}
        )
    else:
        crawled = await scripture.capture_urls.find_one(
            {"hotel_id": capture_id}
        )
    if not crawled:
        logger.warning("Bad crawled id %s", capture_id)
        return {"status": 400, "errmsg": "Invalid capture_id"}
    targets = ["www.hotels.cn", "www.hotels.com"]
    hid = re.match("\d+", url)
    if hid:
        hid = hid.group()
        cn_url = f"https://www.hotels.cn/ho{hid}"
        en_url = f"https://www.hotels.com/ho{hid}/?pos=HCOM_US&locale=en_US"    
    else:
        _url = URL(url)
        if _url.host in targets:
            hid = _url.path.strip("/").split("/")[0][2:]
            cn_url = f"https://www.hotels.cn/ho{hid}"
            en_url = (
                f"https://www.hotels.com/ho{hid}/?pos=HCOM_US&locale=en_US"
            )
        else:
            logger.warning("Bad url %s", url)
            return {"status": 400, "errmsg": "Invalid url"}
    cn_req = requests.get(cn_url)
    cn_req = cn_req.content.decode("utf-8")
    cn_et = etree.HTML(cn_req)
    title = get_log(
        cn_et, field="title", rule=hotels_xp.TITLE, choice="take_first"
    )
    if title == "好订网酒店预订 国际酒店预订 特价国外酒店预订 – 网上订酒店就到Hotels.cn":
        logger.warning("Bad hotel id %s", hid)
        return {"status": 400, "errmsg": "Invalid url"}
    payload = hcom_parse(hid, cn_url, cn_et)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"
    }
    en_req = requests.get(en_url, headers=headers)
    en_req = en_req.content.decode("utf-8")
    en_et = etree.HTML(en_req)
    en_payload = hcom_parse(hid, en_url, en_et)
    payload["url"] = cn_url
    payload["us_url"] = en_url
    payload["en"] = en_payload
    if payload["address_text"] and payload["name"]:
        res = await scripture.hotels.update_one(
            {"hotels_id": hid}, {"$set": payload}, upsert=True
        )
        if res.modified_count:
            await scripture.capture_urls.update_one(
                {"_id": crawled["_id"]},
                {
                    "$set": {
                        "_hotels_cn_id": "",
                        "hotels_cn_id": hid,
                        "bookings_id": "",
                        "_bookings_id": crawled.get("bookings_id"),
                        "jset_id": "",
                        "_jset_id": crawled.get("jset_id"),
                    }
                },
            )
            logger.info(f'hotels_cn_id:{hid} upload success')
            return {"status": 200, "data": payload}
        else:
            logger.info(f'hotels_cn_id:{hid} upload fail')
            return {"status": 500, "errmsg": f"酒店静态数据更新失败!"}
    else:
        if not payload["name"]:
            logger.error(f"酒店名称抓取失败，url：{en_url},xpath:{hotels_xp.NAME}")
        if not payload["address_text"]:
            logger.error(f"酒店名称抓取失败，url：{en_url},xpath:{hotels_xp.ADDRESS}")
        return {"status": 500, "errmsg": f"酒店静态数据更新失败!"}


def hcom_parse(hid, url, et):
    payload = {}
    _url = URL(url)
    site_prefix = {"cn": "CN", "com": "EN"}
    PREFIX = site_prefix.get(_url.host.split(".")[-1])
    payload["short_introduction"] = get_log(
        et,
        field="short_introduction",
        rule=hotels_xp.SHORT_INTRODUCTION,
        choice="take_first",
    )
    payload["locale"] = PREFIX.lower()
    for_families_list = get_log(
        et, field="for_families_list", rule=hotels_xp.FOR_FAMILIES
    )
    payload["for_families"] = hcom_parse_list(for_families_list)
    payload["hotels_id"] = hid
    address_info = get_log(
        et,
        field="address_info",
        rule=hotels_xp.ADDRESS_INFO,
        choice="take_first",
    )
    address_info = json.loads(address_info)["address"]
    payload["city"] = address_info.get("addressLocality")
    title = get_log(
        et, field="title", rule=hotels_xp.TITLE, choice="take_first"
    )
    picture_list = get_log(et, field="picture", rule=hotels_xp.PICTURES)
    payload["picture"] = hcom_pictures(picture_list)
    payload["landmarks"] = get_log(
        et, field="landmarks", rule=hotels_xp.LANDMARKS
    )
    amenities_list = get_log(
        et, field="amenities_list", rule=hotels_xp.AMENITIES
    )
    payload["amenities"] = hcom_parse_list(amenities_list)
    position = get_log(
        et, field="position", rule=hotels_xp.POSITION, choice="take_first"
    )
    latitude, longitude = position.split(",")
    payload["latitude"] = latitude
    traffic_tips_list = get_log(
        et, field="traffic_tips_list", rule=hotels_xp.TRAFFIC_TIPS
    )
    payload["traffic_tips"] = hcom_parse_list(traffic_tips_list)
    payload["notice"] = hcom_notice(et, prefix=PREFIX)
    star = get_log(et, field="star", rule=hotels_xp.STAR, choice="take_first")
    around_list = get_log(et, field="around_list", rule=hotels_xp.AROUND)
    payload["around"] = hcom_parse_list(around_list)
    payload["price"] = get_log(
        et, field="price", rule=hotels_xp.PRICE, choice="take_first"
    )
    address = {}
    address["street"] = address_info.get("streetAddress")
    address["locality"] = address_info.get("addressLocality")
    address["region"] = address_info.get("addressRegion")
    address["postal_code"] = address_info.get("postalCode")
    address["country"] = address_info.get("addressCountry")
    payload["address"] = address
    payload["name"] = get_log(
        et, field="name", rule=hotels_xp.NAME, choice="take_first"
    )
    payload["country"] = address_info.get("addressCountry")
    payload["longitude"] = longitude
    payload["summary"] = hcom_summary(et)
    payload["room_service_facilities"] = hcom_service_facilities(
        et, PREFIX, choice="room_service_facilities"
    )
    payload["in_store_service_facilities"] = hcom_service_facilities(
        et, PREFIX, choice="in_store_service_facilities"
    )
    payload["address_text"] = hcom_address_text(et, prefix=PREFIX)
    try:
        payload["star"] = re.match("(\d+)", star).group()
        payload["title"] = title.split("|")[0]
    except Exception:
        pass
    return payload


def hcom_address_text(et, prefix):
    if prefix == "CN":
        return get_log(
            et,
            field="address_text",
            rule=hotels_xp.ADDRESS,
            choice="take_first",
        )
    elif prefix == "EN":
        ret = get_log(et, field="address_text", rule=hotels_xp.EN_ADDRESS)
        try:
            return reduce(lambda x, y: x + y, map(lambda x: x.strip(), ret))
        except Exception:
            pass


def get_log(et, field=None, rule=None, choice=None):
    logger = logging.getLogger(__name__)
    if choice is None:
        ret = et.xpath(rule)
        if ret:
            return ret
        else:
            logger.warning(f"{field}解析失败，xpath：{rule}")
    elif choice == "take_first":
        try:
            ret = et.xpath(rule)[0]
            return ret
        except Exception:
            logger.warning(f"{field}解析失败，xpath：{rule}")
    elif choice == "nolog":
        try:
            ret = et.xpath(rule)[0]
            return ret
        except Exception:
            pass


def hcom_parse_list(el_list, choice=None):
    try:
        ret = list(map(lambda x: x.xpath("string(.)"), el_list))
    except Exception:
        ret = None
    if choice is None:
        return ret
    elif choice == "dupefilter":
        ret = list(set(ret))
        return ret


def hcom_service_facilities(et, prefix, choice):
    ret = {}
    sf_list = []
    if choice == "room_service_facilities":
        ROOM_SERVICES = getattr(hotels_xp, prefix + "_ROOM_SERVICE_FACT")
        sf_list = get_log(
            et, field="room_service_facilities", rule=ROOM_SERVICES
        )
    elif choice == "in_store_service_facilities":
        IN_STORE_SERVICES = getattr(
            hotels_xp, prefix + "_IN_STORE_SERVICE_FACT"
        )
        sf_list = get_log(
            et, field="in_store_service_facilities", rule=IN_STORE_SERVICES
        )
    if sf_list:
        for value in sf_list:
            k = get_log(
                et=value,
                field="room_service_facilities_title",
                rule=f".{hotels_xp.SERVICE_FACT_TITLE}",
                choice="take_first",
            )
            v = get_log(
                et=value,
                field="room_service_facilities_title",
                rule=f".{hotels_xp.SERVICE_FACT_CELL}",
            )
            ret[k] = v
        return ret


def hcom_clean(_list):
    if not _list:
        return None
    return list(map(lambda v: remove_tags(v), _list))


def hcom_notice(et, prefix):
    keys = {
        "CN": {
            "term": "政策",
            "alias": "其它名称",
            "mandatory": "强制消费",
            "optional": "其它费用",
        },
        "EN": {
            "term": "term",
            "alias": "alias",
            "mandatory": "mandatory fees",
            "optional": "optional fees",
        },
    }
    key = keys[prefix]
    term_xp = getattr(hotels_xp, prefix + "_TERM")
    alias_xp = getattr(hotels_xp, prefix + "_ALIAS")
    mandatory_xp = getattr(hotels_xp, prefix + "_MANDATORY_FEES")
    optional_xp = getattr(hotels_xp, prefix + "_OPTIONAL_FEES")
    term = hcom_parse_list(et.xpath(term_xp), choice="dupefilter")
    alias = hcom_parse_list(et.xpath(alias_xp), choice="dupefilter")
    mandatory = hcom_parse_list(et.xpath(mandatory_xp), choice="dupefilter")
    optional = hcom_parse_list(et.xpath(optional_xp), choice="dupefilter")
    return {
        key["term"]: term,
        key["alias"]: alias,
        key["mandatory"]: mandatory,
        key["optional"]: optional,
    }


def hcom_pictures(selectors):
    _pics = []
    try:
        for select in selectors:
            url = get_log(
                et=select,
                field="url",
                rule="./@data-desktop",
                choice="take_first",
            )
            if not url:
                url = get_log(
                    et=select,
                    field="url",
                    rule="./img/@src",
                    choice="take_first",
                )
            sizes = get_log(
                et=select, field="sizes", rule="./@data-sizes", choice="nolog"
            )
            sizes = sizes and list(sizes) or list("zwybndeglst")
            name = get_log(
                et=select,
                field="name",
                rule='./p/span[@class="room-name"]/text()',
                choice="nolog",
            )
            tag = get_log(
                et=select,
                field="tag",
                rule='./p/span[@class="second-level"]/text()',
                choice="nolog",
            )
            if not name:
                name = get_log(
                    et=select, field="name", rule="./p/text()", choice="nolog"
                )
            u = URL(url)
            if u.host != "exp.cdn-hotels.com":
                *_, uri = u.path.split("/", 6)
                url = str(
                    URL.build(
                        scheme="https", host="exp.cdn-hotels.com", path=uri
                    )
                )
            else:
                url = url.format(size=sizes[0])
            _pics.append(
                {
                    "url": url,
                    "name": name,
                    "classification": tag,
                    "sizes": sizes,
                }
            )
        return _pics
    except Exception:
        pass


def hcom_summary(et):
    key_facts_list = get_log(
        et, field="key_facts", rule=hotels_xp.SUMMARY_KEY_FACTS
    )
    travellings_list = get_log(
        et, field="travellings", rule=hotels_xp.SUMMARY_TRAVELLING
    )
    transport_list = get_log(
        et, field="transport", rule=hotels_xp.SUMMARY_TRANSPORT
    )
    return {
        "key_facts": hcom_clean(hcom_parse_list(el_list=key_facts_list)),
        "travellings": hcom_clean(hcom_parse_list(el_list=travellings_list)),
        "transport": hcom_clean(hcom_parse_list(el_list=transport_list)),
    }


def remove_line_break(s):
    if isinstance(s, list):
        s = "\n".join(s)
    return re.sub(r"\s{2,}", "\n", s).strip()


def find_polices(et):
    policy_base_node = et.xpath('//*[@id="hotelPoliciesInc"]')
    if not policy_base_node:
        return []
    else:
        policy_base_node = policy_base_node[0]
    polices = []
    checkin_out_policy = ""
    for e in policy_base_node.getchildren():
        ori_policy = (
            remove_line_break(e.xpath("string(.)"))
            .replace("预订取消/\n预付政策", "预订取消/预付政策")
            .replace("&amp;", "&")
        )
        if not ori_policy:
            continue
        if 'children' in e.attrib.get('id', ''):
            ori_policy = booking_children_policy(e)
            polices.append(
                {
                    'type': '儿童和加床',
                    'content': ori_policy
                }
            )
            continue
        ori_policy = ori_policy.split("\n")
        if ori_policy[0] == "入住时间":
            checkin_out_policy += f"入住时间: {ori_policy[1]}\n"
            continue
        if ori_policy[0] == "退房时间":
            checkin_out_policy += f"退房时间: {ori_policy[1]}\n"
            continue
        _policy = {
            "type": ori_policy[0],
            "content": "\n".join(set(ori_policy[1:])),
        }
        if _policy["content"].strip() == "":
            continue
        polices.append(_policy)
    polices.append({"type": "入住政策", "content": checkin_out_policy.strip()})
    if et.xpath('//*[@id="hp_important_info_box"]/div[1]/div/text()'):
        polices.append(
            {
                "type": "预定须知",
                "content": remove_line_break(
                    "".join(et.xpath(
                        '//*[@id="hp_important_info_box"]/div[1]/div/text()'
                    ))
                ),
            }
        )
    remove_policy = []
    for i, policy in enumerate(polices):
        if "直至另行通知" in policy["content"]:
            remove_policy.append(i)
            continue
        if "接受上述银行卡" in policy["content"]:
            cards = "、".join(
                et.xpath('//button[@aria-label][@role="img"]/@aria-label')
            )
            policy["content"] = f"{cards}\n{policy['content']}"

    return polices


def booking_children_policy(node):
    if node.xpath('.//table'):
        mid_text = booking_children_policy_table_formater(node.xpath('.//table')[0])
        front_text = remove_line_break(node.xpath('.//div[@class="general-child-policy"]//text()'))
        end_text = remove_line_break(node.xpath('.//div[@class="bed-allowance"]//text()'))
        return f"{front_text}\n{mid_text}\n{end_text}"
    else:
        text = remove_line_break([t for t in node.xpath('.//text()') if t != '免费！']).replace('儿童和加床\n', '')
        return text.replace('\n\n', '\n')


def booking_children_policy_table_formater(node):
    logger = logging.getLogger(__name__)
    text = ""
    for tr in node.xpath('.//tr'):
        tds = tr.xpath('.//td')
        if len(tds) == 3:
            fst = remove_line_break(tds[0].xpath('string(.)')).replace('\n', '')
            sed = remove_line_break(tds[1].xpath('string(.)')).replace('\n', '')
            trh = remove_line_break(tds[2].xpath('string(.)')).replace('\n', '')
            text += f"\n{remove_line_break(fst)}{remove_line_break(sed)}{remove_line_break(trh)}"
        elif len(tds) == 2:
            fst = "; 或"
            sed = remove_line_break(tds[0].xpath('string(.)')).replace('\n', '')
            trh = remove_line_break(tds[1].xpath('string(.)')).replace('\n', '')
            text += f"{remove_line_break(fst)}{remove_line_break(sed)}{remove_line_break(trh)}"
        else:
            logger.error(f"{tr.xpath('string(.)')} has diffren len(tr)")
    return text

async def forrmat_relux_rooms(ori_rooms_cn, ori_rooms_en):
    rooms = []
    rooms_cn = {room['id']: room for room in ori_rooms_cn}
    rooms_en = {room['id']: room for room in ori_rooms_en}
    for rid, room in rooms_cn.items():
        room_type_en = rooms_en.get(rid, {}).get('name', '')
        if any([word in room.get('name', '') for word in relux_room_type_word]):
            room_type = rooms_en.get(rid, {}).get('name', '')
        else:
            room_type = (
                room.get('name', "").replace('room', '')
                .replace('Room', '').replace('可吸烟', '')
                .replace('吸烟/', '').replace('吸烟', '')
                .replace('()', '').replace('（）', '')
                .replace('[]', '').replace('【】', '')
            )
            for word in room_type_en.split():
                room_type = room_type.replace(word, '')
            room_type = room_type.strip()
        gallery = [{'image_url': pic.get('url', '')} for pic in room.get('pictures', [])]
        for i, url in enumerate(
            executor.map(
                transfor_pic_url, gallery
            )
        ):
            gallery[i]['image_url'] = url
        room_desc = room.get('description', '')
        occupancy_info = room.get('capacity', {}).get('max', 2)
        room_size = room.get('sqm', "")
        rooms.append({
            'room_type': room_type,
            'room_type_en': room_type_en,
            'gallery': gallery,
            'room_desc': room_desc,
            'occupancy_info': occupancy_info,
            'room_size': room_size,
        })
    return rooms


def fetch_relux_comment(hid):
    result = []
    resp = requests.get(f"http://www.rlx.jp/{hid}/?lang=zh-cn")
    et = etree.HTML(resp.content.decode('utf-8'))
    comments = et.xpath('//div[@id="review"]')
    if not comments:
        return False
    comments = comments[0]
    rating = "".join([e.strip() for e in comments.xpath('.//div[@class="piechart"]//text()') if e.strip()]).split('/')[0]
    for comment in comments.xpath('.//div[@class="reviewEntry js-reviewEntry"]'):
        _rating = len(comment.xpath('.//span[@class="on"]/img'))
        published_by = comment.xpath('.//p[@class="name"]//text()')
        published_at = comment.xpath('.//p[@class="date"]//text()')
        description = comment.xpath('.//p[@class="date"]/following-sibling::p[1]//text()')
        if published_by and published_at and description:
            result.append(
                {
                    'title': '',
                    'description': "".join(description).strip(),
                    'rating': _rating,
                    'published_at': published_at[0].split('：')[-1],
                    'published_by': published_by[0],
                    'locale': 'jpn',
                }
            )
    return rating, result


def fix_relux_facility(facility):
    new_facility = []
    for faci in facility:
        content = faci['facility'].replace('◆', '').replace('★', '').replace('・', '').replace('~', '').replace('※', '').replace('～', '')
        if len(content) > 4:
            continue
        elif content in [
            '温泉税',
        ]:
            continue
        else:
            new_facility.append(
                {'facility': content}
            )
    return new_facility


def fix_relux_policy_traffic(data, field):
    new_data = []
    for msg in data:
        p_type = msg.get('type', '') or msg.get('traffic', '')
        p_content = msg.get('content', '') or msg.get('destination', '')
        if not p_content.strip():
            continue
        p_content = p_content.replace('◆', '').replace('★', '').replace('・', '').replace('~', '').replace('※', '').replace('～', '')
        if field == 'policy':
            new_data.append({
                'type': p_type,
                'content': p_content
            })
        elif field == 'traffic':
            new_data.append({
                'traffic': p_type,
                'destination': p_content
            })
    return new_data
