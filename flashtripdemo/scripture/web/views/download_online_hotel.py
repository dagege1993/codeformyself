# conding: utf8

from datetime import datetime
from io import BytesIO
import logging

import xlwt
from sanic.response import html, raw
from tasks.inventories import hotel_online_check

from web import settings
from web.utils.database import databases

from . import views_bp

H = """<h1>下载线上酒店excel</h1>
<form taget="_self" method="post" enctype="multipart/form-data">
<button>下载excel</button>
</form>
</a>
<form action="/views/hotel/online/refresh" taget="_self" method="post" enctype="multipart/form-data">
<button>刷新数据</button>
</form>
"""
max_missed = 7
quotes_url = settings.QUOTES_API
headers = {"x-request-from": "order"}


@views_bp.get("/hotel/online")
async def crawl_hcom(request):
    return html(H)


@views_bp.post("/hotel/online")
async def start_crawl_hcom(request):
    logger = logging.getLogger(__name__)
    db = databases("scripture")
    wb = xlwt.Workbook(encoding="utf-8")
    st = wb.add_sheet("sheet1")
    st.write(0, 0, "酒店网址")
    st.write(0, 1, "酒店中文名称")
    st.write(0, 2, "酒店英文名称")
    st.write(0, 3, "酒店中文地址")
    st.write(0, 4, "酒店英文地址")
    row = 1

    base_day = datetime.now().strftime("%Y-%m-%d")
    base_day = datetime.strptime(base_day, "%Y-%m-%d")
    is_refreshing = await db["hotel.online.check"].find_one(
        {"__t": "flag"}, {"refreshing": "1"}
    )

    hotels = []
    async for hotel in db["hotel.online.check"].find(
        {"updated_at": {"$gte": base_day}}
    ):
        hotels.append(hotel)
    if not hotels:
        await db["hotel.online.check"].update_one(
            {"__t": "flag"}, {"$set": {"refreshing": True}}
        )
        hotel_online_check.delay()
        logger.info(f'base_day:{base_day},数据更新')
        return html("""</a>数据更新中，请稍后刷新页面下载excel""")
    for online in hotels:
        st.write(
            row, 0, f"https://flashtrip.cn/hotels/{online.get('_id', '')}"
        )
        st.write(row, 1, online.get("name", ""))
        st.write(row, 2, online.get("name_en", ""))
        st.write(row, 3, online.get('address', ""))
        st.write(row, 4, online.get('en', {}).get('address', ''))
        row += 1
    excel = BytesIO()
    wb.save(excel)
    excel.seek(0)
    logger.info(f'下载酒店信息成功,filename={base_day}上线状态酒店.xls')
    return raw(
        excel.getvalue(),
        headers={
            "Content-Disposition": f"attachment;filename={base_day}上线状态酒店.xls"
        },
        content_type="application/vnd.ms-excel",
    )


@views_bp.post("/hotel/online/refresh")
async def refresh_datas(request):
    logger = logging.getLogger(__name__)
    db = databases("scripture")
    is_refreshing = await db["hotel.online.check"].find_one(
        {"__t": "flag"}, {"refreshing": "1"}
    )
    if not is_refreshing or not is_refreshing.get("refreshing"):
        hotel_online_check.delay()
    logger.info(f'数据更新')
    return html("""</a>数据更新中，请稍后刷新页面下载excel""")



async def get_supplier():
    hub = databases('hub')
    hotels = []
    city_map = {}
    country_map = {}
    async for hotel in hub['poi_items'].find(
        {"__t": "Hotel", "edit_status": {"$in": ["edited", "audited"]},
         "publish_status": "online"},{'name': '1', 'address': '1', 'name_en': '1', 'quote_ids': '1', 'city': '1'}
    ):
        if hotel['city'] not in city_map:
            city_name = await hub['meta_cities'].find_one({'_id': hotel['city']}, {'name': '1', 'country': '1'})
            if not city_name:
                city_map[hotel['city']] = '已删除'
                country_map[hotel['city']] = '已删除'
            else:
                city_map[hotel['city']] = city_name['name']
                country_name = await hub['meta_countries'].find_one({"_id": city_name['country']}, {'name': '1'})
                country_map[hotel['city']] = country_name['name']
        line = {
                 0: str(hotel['_id']),
                 1: hotel['name'],
                 2: hotel['name_en'],
                 3: hotel['address'],
                 4: city_map[hotel['city']],
                 14: country_map[hotel['city']]
             }
        for quote in hotel['quote_ids']:
            line[settings.SUPPLIER_ID_2_INDEX[str(quote['quoter'])]] = str(quote['hotel_id'])
        hotels.append(line)
    return hotels

@views_bp.get('/hotels/online/supplier')
async def get_online_supplier(request):
    logger = logging.getLogger(__name__)
    wb = xlwt.Workbook(encoding="utf-8")
    st = wb.add_sheet("sheet1")
    st.write(0, 0, 'cmsID')
    st.write(0, 1, '酒店名称')
    st.write(0, 2, '英文名称')
    st.write(0, 3, '酒店地址')
    st.write(0, 4, '酒店所属城市')
    st.write(0, 14, '酒店所属国家')
    st.write(0, 5, 'hotelbeds')
    st.write(0, 6, 'hotelspro')
    st.write(0, 7, 'relux')
    st.write(0, 8, 'bonotel')
    st.write(0, 9, 'jactravel')
    st.write(0, 10, 'roomsxml')
    st.write(0, 11, 'weegotr')
    st.write(0, 12, 'whotel')
    st.write(0, 13, 'travflex')
    hotels = await get_supplier()
    for row, data in enumerate(hotels):
        for col, msg in data.items():
            st.write(row+1, col, msg)
    excel = BytesIO()
    wb.save(excel)
    excel.seek(0)
    logger.info(f'下载酒店信息成功,filename=上线酒店供应商统计.xls')
    return raw(
        excel.getvalue(),
        headers={
            "Content-Disposition": f"attachment;filename=上线酒店供应商统计.xls"
        },
        content_type="application/vnd.ms-excel",
    )