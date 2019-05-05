import pandas as pd

import requests
import scrapy
import pymysql
from datetime import date

city_dict = {
    "涪陵区": "重庆市", "江津区": "重庆市", "沙坪坝区": "重庆市", "大渡口区": "重庆市", "渝北区": "重庆市",
    "万州区": "重庆市", "永川区": "重庆市", "巴南区": "重庆市", "北碚区": "重庆市", "南岸区": "重庆市",
    "渝中区": "重庆市", "江北区": "重庆市", "合川区": "重庆市", "南川区": "重庆市",
    "长寿区": "重庆市", "九龙坡区": "重庆市", "万盛区": "重庆市",

    "宝山区": "上海市", "闵行区": "上海市", "松江区": "上海市", "嘉定区": "上海市", "青浦区": "上海市", "普陀区": "上海市", "浦东新区": "上海市",
    "杨浦区": "上海市", "金山区": "上海市", "黄浦区": "上海市",

    "大兴区": "北京市", "房山区": "北京市", "石景山区": "北京市", "丰台区": "北京市", "昌平区": "北京市", "顺义区": "北京市",
    "朝阳区": "北京市", "通州区": "北京市", "海淀区": "北京市",

    "滨海新区": "天津市", "北辰区": "天津市", "河西区": "天津市",
    "东丽区": "天津市", "武清区": "天津市", "南开区": "天津市",
    "铜仁地区": "铜仁市",
}


def start_project():
    url = "http://www.yonghui.com.cn/2008_store.asp"
    querystring = {"action": "3"}
    payload = ""
    headers = {
        'Cookie': "ASPSESSIONIDACQCBQTB=JLAOFJAAIMNNBOELPJDIELDL; UM_distinctid=1683b18a72550d-0e7c78c7ce895f-b781636-1fa400-1683b18a726345; CNZZDATA2308581=cnzz_eid%3D2084446436-1547175326-null%26ntime%3D1547175326; ASPSESSIONIDACRACSTD=CENLGCCANMKIIOGIEJJKEJKM",
        'Host': "www.yonghui.com.cn",
        'Upgrade-Insecure-Requests': "1",
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
        'cache-control': "no-cache",
        # 'Postman-Token': "d7251410-9c7f-4dcc-b185-023b12b104b1"
    }

    response = requests.request("GET", url, data=payload, headers=headers, params=querystring)
    page_source = response.content.decode(response.apparent_encoding, 'ignore')
    storage(page_source)


def storage(page_source):
    page_sel = scrapy.Selector(text=page_source)
    shop_list = page_sel.xpath(
        "//table[contains(@width, '747') and contains(@height, '24')and contains(@border, '0')and contains(@cellpadding, '0')]").extract()
    del shop_list[0: 2]  # 只删除第0和第1个元素
    city_level_dict = get_city_level()
    print(len(shop_list))
    for shop in shop_list:
        shop_detail = scrapy.Selector(text=shop)
        shop_name = shop_detail.xpath("//td[contains(@width,'148')]//@title").extract_first()
        name = shop_name.split(' ')[1]
        city = shop_name.split(' ')[0]
        if "区" in city:
            city_myself = city_dict.get(city)
            if city_myself:
                city = city_myself
            else:
                print('还未记录的区', city)
        shop_address = shop_detail.xpath("//td[contains(@width,'322')]//@title").extract_first()
        shop_open_time = shop_detail.xpath("//td[contains(@width,'72')]//text()").extract()[1]
        if '筹建中门店' in shop_open_time:
            open_or_not = 0
        else:
            open_or_not = 1
        format_city = city.split("市")[0]  # 把市去掉
        city_level = city_level_dict.get(format_city)
        if city_level:
            pass
        else:
            city_level = "四/五线城市"
        insert_sql = """insert into YongHui (city, open_or_not,shop_name,shop_open_time,address,crawlTime,city_level) VALUES ("%s","%s","%s","%s","%s","%s","%s") """ % (
            city, open_or_not, name, shop_open_time, shop_address, crawl_time, city_level)
        cursor.execute(insert_sql)


def get_city_level():
    path = r'city_level.xlsx'
    results = pd.read_excel(path)
    city_list = results['城市']
    level_list = results['城市等级']
    city_level_dict = dict(zip(city_list, level_list))
    print(city_level_dict)
    return (city_level_dict)


if __name__ == '__main__':
    db = pymysql.connect(host='192.168.103.31', user='root', password="adminadmin",
                         database='shops')
    cursor = db.cursor()
    crawl_time = date.today()
    print("抓取时间", crawl_time)
    start_project()
