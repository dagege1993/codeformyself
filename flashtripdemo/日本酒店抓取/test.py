import re
import time
from datetime import datetime

import pymongo
import requests
import scrapy
from pymongo import MongoClient

base_url = 'https://www.japanican.com'
lost_hotel = []
client = MongoClient(host='localhost', port=27017)
db_auth = client.admin
db = client['scripture']['statics.hotels.relux_add']


def get_hotel(id, hotel_name):
    headers = {
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Referer': 'https://www.japanican.com/cn/hotel/list/?navcheckin=&navcheckout=&sn=1&rn=1&apn=2&hcpn=0&cbn=0&anl=%E9%99%B6%E6%B3%89%20%E5%BE%A1%E6%89%80%E5%9D%8A',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    }

    params = (
        ('navcheckin', ''),
        ('navcheckout', ''),
        ('sn', '1'),
        ('rn', '1'),
        ('apn', '2'),
        ('hcpn', '0'),
        ('cbn', '0'),
        ('anl', hotel_name),
    )
    # 搜索页面,输入酒店名称
    response = requests.get('https://www.japanican.com/cn/hotel/list/', headers=headers, params=params)
    if '很遗憾，没有找到符合您设定条件的住宿。请重新设定条件再次搜索' in response.text:
        lost_hotel.append(hotel_name)
    else:  # 如果有搜索到的酒店
        page_sel = scrapy.Selector(text=response.text)
        response_xp = page_sel.xpath(
            '//*[@id="hotel_main_0_HotelListRepeater_HotelListName_0"]/dl/dt/a/@href').extract_first()
        hotel_url = base_url + response_xp
        detail_response = requests.get(hotel_url, headers=headers, params=params)
        detail_response_text = detail_response.text
        item = xpath_detail(detail_response_text, hotel_url)  # 自定义解析函数,返回解析后的item

        if '期待您的点评' in detail_response_text:  # 这样就是没有评论,直接评论为空
            comment_dict_list = ''
        else:  # 如果有评论,就进入评论详情页
            hotel_id = re.findall('"ChikuShisetsu":"(.*?)"', detail_response_text)
            comment_url = 'https://www.japanican.com/cn/hotel/review/' + hotel_id[0] + '/?so=h&rn=1&apn=2&hcpn=0&cbn=0'
            comment_response = requests.get(comment_url, headers=headers)
            comment_response_text = comment_response.text
            comment_response = scrapy.Selector(text=comment_response_text)
            comment_list = comment_response.xpath('//*[@class="reviewModule"]').extract()
            comment_dict_list = []
            for comment in comment_list:
                comment_dict = {}
                comment = scrapy.Selector(text=comment)
                name = comment.xpath('//*[@class="name"]/text()').extract_first()
                star = comment.xpath('//*[@class="reviewStars"]//text()').extract_first()
                user_comment = comment.xpath('//*[@class="comment"]//text()').extract_first()
                if user_comment is None:
                    pass
                else:
                    user_comment = user_comment.replace('/n', '').strip()
                    result = check_contain_chinese(user_comment)
                    if result is True:
                        locale = '中文'
                    else:
                        locale = '英文'
                    time = comment.xpath('/html/body/div/table/tbody/tr[1]/td[1]/text()').extract_first()
                    comment_dict['published_by'] = name
                    comment_dict['rating'] = star
                    comment_dict['description'] = user_comment
                    comment_dict['published_at'] = time
                    comment_dict['locale'] = locale
                    comment_dict['title'] = ''
                    comment_dict_list.append(comment_dict)

            comment_dict_list = [comment_dict for comment_dict in comment_dict_list if
                                 comment_dict['description'] != '']  # 评论不为空
            comment_dict_list = [comment_dict for comment_dict in comment_dict_list if
                                 len(comment_dict['description']) > 2]  # 评论区长度需要>2
            comment_dict_list = comment_dict_list[0:5]  # 最后再取5个
        # 最后入库
        db.update_one(
            {
                "hotel_url": hotel_url
            },
            {"$set": {
                'image_list': item['image_list'],
                'accss_info': item['accss_info'],
                'name_ch': item['name_ch'],
                'name_en': item['name_en'],
                'facilities': item['facilities'],
                'hotel_desc': item['hotel_desc'],
                'city': item['city'],
                'comments': comment_dict_list,
                'code': id,

            },
                "$setOnInsert": {"created_at": datetime.now()},
                "$currentDate": {"updated_at": True}},
            upsert=True,
        )
    print('搜索不到的酒店', hotel_name)


# 自定义解析函数,返回item
def xpath_detail(detail_response_text, hotel_url):
    page_sel = scrapy.Selector(text=detail_response_text)
    facility_list = page_sel.xpath("//*[@class='facility_info_tables']").extract()
    del (facility_list[0])
    facility_desc_lis = []
    for i in (facility_list):
        if '建筑物构造' not in i and '其他可接受信用卡种类' not in i:
            page_lisgt = scrapy.Selector(text=i)
            facility_desc = page_lisgt.xpath('*//table/tr/th/text()').extract()
            facility_desc = (','.join(facility_desc).strip())
            facility_desc_lis.append(facility_desc)
    fa_info = page_sel.xpath('*//ul[@id="hotel_contents_0_IconUl"]/li/text()').extract()
    fa_info = ','.join(fa_info)
    facility_desc_lis.append(fa_info)
    facility_desc_lis = [{'facility': facility_desc} for facility_desc in facility_desc_lis if facility_desc != '']
    image_list = re.findall('https:\/\/.*?jpg', detail_response_text)
    image_list = list(set(image_list))
    image_list = [{'image_url': image} for image in image_list]
    accss_info = page_sel.xpath('*//p[@class="hotelinfo__access"]/a/text()').extract_first()
    name_info = page_sel.xpath('*//h1[@class="hotelinfo__name"]/span/text()').extract_first()
    name_ch = name_info.split('/')[0]
    name_en = name_info.split('/')[1]
    hotel_url = hotel_url
    hotel_desc = page_sel.xpath('*//p[@id="hotel_contents_0_SalesPointParagraph"]/text()').extract_first()
    hotel_desc2 = page_sel.xpath('*//div[@id="hotel_contents_0_Information"]/text()').extract_first()
    hotel_desc3 = page_sel.xpath('*//div[@id="hotel_contents_0_hotel_main_1_AccessParagraph"]//text()').extract()
    hotel_desc3 = ','.join(hotel_desc3)
    if hotel_desc2 is None:  # 不加
        hotel_desc = hotel_desc + ',' + hotel_desc3
    else:
        hotel_desc = hotel_desc + ',' + hotel_desc2 + ',' + hotel_desc3
    city = page_sel.xpath('//*[@itemtype="http://data-vocabulary.org/Breadcrumb"]/li/a/text()').extract()
    city = city[2].strip()
    policy = page_sel.xpath('//*[@id="hotel_contents_0_EmergencyInformation"]/dl/dd/text()').extract()
    policy_children = page_sel.xpath('//*[@style="display:inline;"]/text()').extract()
    policy_children = [policy.replace('\n', '').strip() for policy in policy_children]

    if '有关儿童入住规定:接受儿童入住' in policy_children and '有关儿童入住规定:不接受儿童入住' in policy_children:
        policy_children = ['部分房型不接受儿童']
    else:
        policy_children = policy_children[0]
    hotel_info = {}
    hotel_info['image_list'] = image_list
    hotel_info['accss_info'] = accss_info
    hotel_info['name_ch'] = name_ch
    hotel_info['name_en'] = name_en
    hotel_info['hotel_url'] = hotel_url
    hotel_info['facilities'] = facility_desc_lis
    hotel_info['hotel_desc'] = hotel_desc
    hotel_info['city'] = city
    hotel_info['policy'] = policy.append(policy_children)
    return hotel_info


# 区别中英文
def check_contain_chinese(check_str):
    for ch in check_str:
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
    return False


# df = pd.read_excel('./c613de64ad0a949c.xlsx')
# hotel_id = df['酒店_id'].tolist()
# hotel_name = df['宿名'].tolist()
# id_name = dict(zip(hotel_id, hotel_name))
# print(id_name)
id_name = {22204: 'ホテルマイステイズプレミア成田', 23722: '品川プリンスホテル', 21962: 'ダイワロイネットホテル銀座', 22244: 'HOTEL POTMUM',
           21561: '西鉄ホテル クルーム博多', 23739: 'センチュリオンホテルリゾートヴィンテージ沖縄美ら海', 21878: '三井ガーデンホテル 京橋', 22246: 'コンドミニアムホテル モンパ',
           22801: '芦ノ湖畔蛸川温泉 龍宮殿', 23165: 'プレミアホテル-CABIN-新宿', 22146: '有馬温泉 元湯 古泉閣', 21771: '小豆島国際ホテル',
           21829: '三井ガーデンホテル上野', 22032: 'マイステイズ新浦安コンファレンスセンター', 22735: '旅亭 花ゆら',
           21310: 'ザ パーク フロント ホテル アット ユニバーサル・スタジオ・ジャパン(TM)', 28654: '大阪マリオット都ホテル', 22587: 'ホテル ミクラス',
           21557: 'ホテルマイステイズプレミア金沢', 21135: 'ヒルトン大阪', 22131: 'ORIENTAL HOTEL', 23547: 'リッチモンドホテル札幌大通',
           22845: 'ホテルトラスティ大阪阿倍野', 21643: 'フサキビーチリゾート ホテル＆ヴィラズ', 22786: 'サンシャインシティプリンスホテル', 22824: 'ホテルWBF東京浅草',
           21895: '阿蘇ファームヴィレッジ', 21443: '三井ガーデンホテル名古屋プレミア', 21943: '函館国際ホテル', 26634: '富士レークホテル', 23378: 'ホテルグレイスリー那覇',
           23296: 'ホテルリリーフ札幌すすきの', 23658: 'ホテル京阪 札幌', 23769: 'ONSEN RYOKAN YUEN SHINJUKU', 21591: '箱根・芦ノ湖 はなをり',
           23652: 'ホテル京阪 京都八条口', 22412: 'ホテルマイステイズ舞浜', 22194: '海の旅亭 おきなわ名嘉真荘', 23081: 'ダイワロイネットホテル西新宿',
           22001: 'アートホテル石垣島', 23237: 'ふふ 河口湖', 22526: 'ホテル・アンドルームス名古屋栄', 23655: 'ホテル京阪 浅草', 21081: 'リッチモンドホテルプレミア浅草',
           22879: 'ココシャスモンパ', 23428: 'ホテルウィングインターナショナルセレクト浅草駒形', 21386: 'ホテルメトロポリタンエドモント', 28564: '東京ステーションホテル',
           28977: '琵琶湖ホテル', 21780: 'ヒルトン東京お台場', 23599: 'ベッセルイン札幌中島公園', 23214: 'プレミアホテル-CABIN-大阪', 26300: '札幌グランドホテル',
           22474: '変なホテル東京 銀座', 22688: 'ホテルマイステイズ神田', 23083: 'ダイワロイネットホテル東京有明', 22450: '横浜ロイヤルパークホテル',
           21470: 'なんばオリエンタルホテル', 21937: 'ハイアット リージェンシー 那覇 沖縄', 22693: 'ホテルマイステイズ札幌駅北口', 22103: 'ホテルレオパレス博多',
           21352: 'ヒルトン東京ベイ', 22164: 'ホテルマイステイズ富士山 展望温泉', 22525: '都ホテル 京都八条（旧 新・都ホテル）', 23707: '静鉄ホテルプレジオ 静岡駅南',
           21936: 'ホテルリソル池袋', 21541: '神戸ポートピアホテル', 21405: 'サンルートプラザ東京', 23898: 'hotel zen tokyo',
           26525: 'ホテルモントレ グラスミア大阪', 21818: 'ホテルグランヴィア京都', 22360: 'センチュリオンホテル クラシック奈良', 21432: '三井ガーデンホテル銀座プレミア',
           21497: '赤坂 エクセルホテル東急', 23190: 'センチュリオンホテル・レジデンシャル赤坂', 22291: 'ホテルソニア小樽', 21453: 'ザ ロイヤルパークホテル 京都三条',
           22751: 'ザ・プリンス パークタワー東京', 21480: 'ラグナガーデンホテル', 26639: 'ソラリア西鉄ホテル銀座', 29182: 'アルモニーアンブラッセ大阪',
           22690: 'ホテルマイステイズ福岡天神南', 22072: 'ダイワロイネットホテルぬまづ', 21641: 'ホテルマイステイズプレミア赤坂', 21283: '函館大沼 鶴雅リゾート エプイ',
           22046: 'ラフォーレ倶楽部 伊東温泉 湯の庭', 23659: 'ホテル京阪 京都 グランデ', 23907: '中部国際空港 セントレアホテル', 23899: '花もみじ',
           21141: 'ヒルトン名古屋', 22530: 'グランドプリンスホテル新高輪', 21782: 'コンラッド大阪', 21108: '京湯元 ハトヤ瑞鳳閣', 22107: 'センチュリオンホテル上野',
           23191: 'センチュリオンホテルグランド赤坂', 27776: '鎌倉パークホテル', 21472: 'クインテッサホテル大阪ベイ', 21190: 'ホテルバリタワー大阪天王寺',
           22157: 'ホテルマイステイズ札幌アスペン', 29983: '京都東急ホテル'}


# 用沙盒的IP访问不了这个网站,所以需要本地跑完,然后用连上VPN,再把本地数据库导入沙盒数据库
def database_change():
    client_local = pymongo.MongoClient(host='localhost', port=27017)
    client_sandbox = pymongo.MongoClient(host='172.16.4.110', port=27017)

    db_local = client_local['scripture']['statics.hotels.relux_add']
    db_sandbox = client_sandbox['scripture']['statics.hotels.relux_add2']

    db_local_results = db_local.find()
    for db_locals in db_local_results:
        db_sandbox.insert(db_locals)


# 主流程函数
def start_crawl():
    # for id, name in id_name.items():
    #     try:
    #         time.sleep(2)
    #         get_hotel(id, name)
    #     except Exception as e:
    #         print(id, name, e)
    # time.sleep(4)
    wait_input = input('是否移动数据:1是转换,0是不转换 ')
    print(wait_input)
    database_change()


if __name__ == '__main__':
    start_crawl()
