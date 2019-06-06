# coding:utf-8
import logging
import requests
from bson import ObjectId
from tasks.application import app
from tasks.utils.database import databases
from tasks import settings
from datetime import datetime

from .hotel_online_check import hotel_check
from .price_calendar import catch_one
from .skyscanner import crawl_one
from .provider import save_prices, provider_booking, compair_ctrip
from .preparation_check import save_preparation_data
from .fix_imp import check_bug_price
from scripture.settings import PRICES_DING_TOKEN

logger = logging.getLogger('celery.task')
Ding_params = {"access_token": PRICES_DING_TOKEN}

@app.task
def hotel_online_check():
    hotel_check()


@app.task
def calendar_one(hotel_id, start_time=None, end_time=None, days=None, do_bug_price=False):
    if not days:
        try:
            resp = requests.get(
                f"{settings.CMS_API}/api/internal/configs/hotel",
                params={"configs": "price_calendar_display_day_span"},
                headers={"accept-version": "6.0.0"},
            )
            if resp and resp.status_code == 200:
                days = resp.json()["data"].get(
                    "price_calendar_display_day_span", 130
                )
        except Exception as exc:
            logger.error(f"get calendar days error!", exc_info=exc)
            days = 130
    catch_one(hotel_id, start_time, end_time, days, do_bug_price)


@app.task
def send_tf_id_errormsg():
    '''
    查询出历史TF酒店ID配错或已失效的数据
    统计完成后从表中删除
    '''
    db = databases('scripture')
    data = db['taskmsg.availability'].find({"type": "travflex_id_error"})
    text = "# 有线上酒店填写的Travflex酒店ID已失效 \n\n"
    nums = 0
    last_updated_time = None
    for e in data:
        if not last_updated_time or e['updated_at'] > last_updated_time:
            last_updated_time = e['updated_at']
        ids.append(e['hotel_id'])
        text += f"- cms链接: http://wop.feifanweige.com/admin/hotels/{e['hotel_id']}\n"
        nums += 1
    payload = {
        "msgtype": "markdown",
        "markdown": {
            "title": "有线上酒店填写的Travflex酒店ID已失效",
            "text": text,
        },
    }
    resp = requests.post(
            "https://oapi.dingtalk.com/robot/send",
            params=Ding_params,
            json=payload,
        )
    db['taskmsg.availability'].remove({"type": "travflex_id_error", "updated_at": {"$lte": last_updated_time}})


@app.task
def calendar_all():
    hub = databases("hub")
    max_num = hub["feature_switch"].find_one(
        {"table": "Activity"}, {"config": "1"}
    )
    try:
        max_num = max_num["config"]["max_price_calendar_hotel"]
    except Exception as exc:
        logger.error(f"cannot get max_num ! ", exc_info=exc)
        exit()
    try:
        resp = requests.get(
            f"{settings.CMS_API}/api/internal/configs/hotel",
            params={"configs": "price_calendar_display_day_span"},
            headers={"accept-version": "6.0.0"},
        )
        if resp and resp.status_code == 200:
            days = resp.json()["data"].get(
                "price_calendar_display_day_span", 130
            )
    except Exception as exc:
        logger.error(f"get calendar days error!", exc_info=exc)
        days = 130
    for hotel in (
        hub["poi_items"]
        .find(
            {"has_price_calendar": True},
            {"quote_ids": "1", "min_booking_days": "1"},
        )
        .sort([("updatedAt", -1)])
        .limit(max_num)
    ):
        calendar_one.delay(str(hotel["_id"]), days=days)


@app.task
def bug_price_one(hotel_id, days=183):
    calendar_one.delay(hotel_id, days=days, do_bug_price=True)
    logger.info(f"publish {hotel_id} for {days} find bug_price")
    return f"{hotel_id} bug price find task publish succeed"

@app.task
def bug_price_all():
    url = f"{settings.CMS_API}/api/internal/special_price_products"
    resp = requests.get(url, headers={"accept-version": "6.0.0"})
    if not resp or resp.status_code != 200 or not resp.json() or resp.json().get('status') != 200:
        logger.error(f"get bug_price hotel id failed! {resp.content}")
        return "get bug_price hotel id failed!"
    for hotel_id in resp.json()['data']:
        calendar_one.delay(hotel_id, days=183, do_bug_price=True)
    logger.info(f"total publish {len(resp.json()['data'])} hotel {resp.json()['data']}")
    return "bug_price_all publish succeed"


@app.task
def preparation_one(**kwargs):
    save_preparation_data(**kwargs)


@app.task
def check_preparation(
    hotels, start_time=None, end_time=None, max_days=None, min_booking_days=1
):
    """
    hotels: [
        {
            'provider': Provider.provider or 'cms' or 'providers'
            'hotel_id': hotel_id or cms_id or id1::provider_id1;id2::provider_id2
        }
    ]
    """
    hub = databases("hub")
    for hotel in hotels:
        if hotel["provider"] == "cms":
            data = hub["poi_items"].find_one(
                {"_id": ObjectId(hotel["hotel_id"])},
                {"quote_ids": "1", "min_booking_days": "1"},
            )
            if not data:
                logger.error(f"not find cms hotel with {hotel['hotel_id']}!")
                continue
            p_hotel = {
                "id": hotel["hotel_id"],
                "hotels": [
                    {"quoter": str(e["quoter"]), "hotel_id": e["hotel_id"]}
                    for e in data["quote_ids"]
                ],
            }
            preparation_one.delay(
                hotel=p_hotel,
                start_time=start_time,
                end_time=end_time,
                max_days=max_days,
                min_booking_days=data.get("min_booking_days", 1),
            )
        elif hotel["provider"] == "providers":
            p_hotel = {"id": hotel["hotel_id"], "hotels": []}
            for _ in hotel["hotel_id"].split(";"):
                hotel_id, provider = _.split("::")
                provider = settings.SUPPLIER_NAME_2_ID.get(provider, provider)
                p_hotel["hotels"].append(
                    {"quoter": provider, "hotel_id": hotel_id}
                )
            preparation_one.delay(
                hotel=p_hotel,
                start_time=start_time,
                end_time=end_time,
                max_days=max_days,
                min_booking_days=min_booking_days,
            )
        else:
            provider = settings.SUPPLIER_NAME_2_ID.get(
                hotel["provider"], hotel["provider"]
            )
            p_hotel = {
                "id": f"{hotel['hotel_id']}::{provider}",
                "hotels": [
                    {"quoter": provider, "hotel_id": hotel["hotel_id"]}
                ],
            }
            preparation_one.delay(
                hotel=p_hotel,
                start_time=start_time,
                end_time=end_time,
                max_days=max_days,
                min_booking_days=min_booking_days,
            )
    return "preparation check publish succeed"


@app.task
def get_skyscanner(start_time, days, sid=None, hotel_id=None, hotel_name=None):
    if not hotel_id and not hotel_name:
        logger.info(f"skyscanner withou hotel_id and name! sid: {sid}")
        return False
    if not sid:
        if hotel_id:
            hub = databases("hub")
            ori_sid = hub["poi_items"].find_one(
                {"_id": ObjectId(hotel_id)}, {"third_ref_ids": "1"}
            )
            if not ori_sid.get("third_ref_ids"):
                logger.info(
                    f"hotel without skyscanner id! hotel_id : {hotel_id}"
                )
                return False
            return crawl_one(
                start_time,
                days,
                ori_sid["third_ref_ids"][0]["value"],
                hotel_id,
                hotel_name,
            )
        scripture = databases("scripture")
        ori_sid = scripture["statics.hotels.skyscanner"].find_one(
            {"name": {"$regex": hotel_name}}, {"sid": "1"}
        )
        if not ori_sid:
            logger.info(
                f"hotel_name not find in skyscanner datas! hotel_name : {hotel_name}"
            )
            return False
        return crawl_one(
            start_time, days, ori_sid["sid"], hotel_id, hotel_name
        )
    else:
        return crawl_one(start_time, days, sid, hotel_id, hotel_name)


@app.task
def get_provider_prices(
    hotel_id=None,
    quoter_id=None,
    hotels=None,
    start_time=None,
    end_time=None,
    days=None,
):
    result = []
    if hotels:
        for hotel in hotels:
            result.append(
                save_prices(
                    hotel_id=hotel['hotel_id'],
                    quoter_id=hotel['quoter'],
                    start_time=start_time,
                    days=days,
                    end_time=end_time,
                )
            )
    if hotel_id and quoter_id:
        result.append(save_prices(
            hotel_id=hotel_id,
            quoter_id=quoter_id,
            start_time=start_time,
            days=days,
            end_time=end_time,
        )
        )
    return result


@app.task
def provider_compair_booking(start_time, days, hotels):
    for hotel in hotels:
        if isinstance(hotel, dict):
            result = provider_booking(
                provider=hotel["provider"],
                start_time=start_time,
                days=days,
                hotel_id=hotel.get("hotel_id"),
                hotel_name=hotel.get("hotel_name"),
                bk_url=hotel.get("bk_url"),
            )
        elif isinstance(hotel, str):
            result = provider_booking(
                provider="cms",
                start_time=start_time,
                days=days,
                hotel_id=hotel,
            )
        logger.info(f"publish booking compair {result} with {hotel}")
    return "done"


@app.task
def provider_compair_ctrip(start_time, days, hotels):
    for hotel in hotels:
        if isinstance(hotel, dict):
            result = compair_ctrip(
                provider=hotel.get("provider") or "cms",
                start_time=start_time,
                days=days,
                hotel_id=hotel.get("hotel_id"),
                hotel_name=hotel.get("hotel_name"),
            )
        elif isinstance(hotel, str):
            result = compair_ctrip(
                provider="cms",
                start_time=start_time,
                days=days,
                hotel_id=hotel,
            )
        logger.info(f"publish ctrip compair {result} with {hotel}")
    return "done"
