import time
from selenium.webdriver.common.keys import Keys

from selenium import webdriver

chrome_options = webdriver.ChromeOptions()
prefs = {"profile.managed_default_content_settings.images": 2}
chrome_options.add_experimental_option("prefs", prefs)
browser = webdriver.Chrome(chrome_options=chrome_options,
                           executable_path='/Users/huangjack/PycharmProjects/codeformyself/flashtripdemo/酒店价格查询/chromedriver')
# browser.set_page_load_timeout(10)
# browser.set_script_timeout(5)
browser.get("https://www.tripadvisor.cn/Lvyou")
lost_city_list = [{'city_name': '五渔村', 'country_name': '意大利', 'err_msg': '没有城市'},
                  {'city_name': '拉斯佩齐亚', 'country_name': '意大利', 'err_msg': '没有城市'},
                  {'city_name': '巴斯', 'country_name': '英国', 'err_msg': '没有城市'},
                  {'city_name': '阿维尼翁', 'country_name': '法国', 'err_msg': '没有城市'},
                  {'city_name': '苏格兰高地', 'country_name': '英国', 'err_msg': '没有城市'},
                  {'city_name': '牛津', 'country_name': '英国', 'err_msg': '没有城市'},
                  {'city_name': '托斯卡纳', 'country_name': '意大利', 'err_msg': '没有城市'},
                  {'city_name': '米克诺斯', 'country_name': '希腊', 'err_msg': '没有城市'},
                  {'city_name': '剑桥', 'country_name': '英国', 'err_msg': '没有城市'},
                  {'city_name': '采尔马特', 'country_name': '瑞士', 'err_msg': '没有城市'},
                  {'city_name': '阿维尼翁', 'country_name': '法国', 'err_msg': '没有城市'},
                  {'city_name': '采尔马特', 'country_name': '瑞士', 'err_msg': '没有城市'},
                  {'city_name': '毛里求斯', 'country_name': '毛里求斯', 'err_msg': '没有城市'},
                  {'city_name': '汤布院', 'country_name': '日本', 'err_msg': '没有城市'},
                  {'city_name': '赛舌儿', 'country_name': '赛舌儿', 'err_msg': '没有此国家'},
                  {'city_name': '函馆', 'country_name': '日本', 'err_msg': '没有城市'},
                  {'city_name': '卡萨布兰卡', 'country_name': '摩洛哥', 'err_msg': '没有此国家'},
                  {'city_name': '马拉喀什', 'country_name': '摩洛哥', 'err_msg': '没有此国家'},
                  {'city_name': '瓦尔扎扎特', 'country_name': '摩洛哥', 'err_msg': '没有此国家'},
                  {'city_name': '舍夫沙万', 'country_name': '摩洛哥', 'err_msg': '没有此国家'},
                  {'city_name': '名古屋', 'country_name': '日本', 'err_msg': '没有城市'},
                  {'city_name': '轻井泽', 'country_name': '日本', 'err_msg': '没有城市'},
                  {'city_name': '西贡', 'country_name': '越南', 'err_msg': '没有城市'},
                  {'city_name': '清迈 ', 'country_name': '泰国', 'err_msg': '没有城市'},
                  {'city_name': '澳门', 'country_name': '中国', 'err_msg': '没有城市'},
                  {'city_name': '伊豆', 'country_name': '日本', 'err_msg': '没有城市'},
                  {'city_name': '长滩岛', 'country_name': '菲律宾', 'err_msg': '没有城市'},
                  {'city_name': '苏梅岛', 'country_name': '泰国', 'err_msg': '没有城市'},
                  {'city_name': '非斯', 'country_name': '摩洛哥', 'err_msg': '没有此国家'},
                  {'city_name': '马尔代夫', 'country_name': '马尔代夫', 'err_msg': '没有城市'},
                  {'city_name': '宿务', 'country_name': '菲律宾', 'err_msg': '没有城市'},
                  {'city_name': '巴厘岛', 'country_name': '印度尼西亚', 'err_msg': '没有城市'},
                  {'city_name': '美奈', 'country_name': '越南', 'err_msg': '没有城市'},
                  {'city_name': '芭提雅', 'country_name': '泰国', 'err_msg': '没有城市'},
                  {'city_name': '香港', 'country_name': '中国', 'err_msg': '没有城市'},
                  {'city_name': '台湾', 'country_name': '中国', 'err_msg': '没有城市'},
                  {'city_name': '热海', 'country_name': '日本', 'err_msg': '没有城市'}]
lost_city_url = []
for lost_city in lost_city_list:
    city_name = lost_city.get("city_name")
    country_name = lost_city.get("country_name")
    # print(city_name)
    try:
        browser.find_element_by_id("destinations_lander_loc_handler").send_keys(city_name)
        time.sleep(1)
        browser.find_element_by_class_name("header-search-submit").click()

        # browser.find_element_by_id("global-nav-hotels").click()
        url = browser.current_url
        url = url.replace('Vacations', 'Hotels').replace('Tourism', 'Hotels')
        result = {'city_name': city_name, 'city_url': url, 'country_name': country_name}
        lost_city_url.append(result)
        browser.back()
        print(lost_city_url)
    except Exception as e:

        print(city_name, '当前城市可能真没有')
        browser.back()
browser.quit()

print(lost_city_url)

lost_city_url_list = \
    [

        {'city_name': '五渔村',
                    'city_url': 'https://www.tripadvisor.cn/Hotels-g187817-Cinque_Terre_Italian_Riviera_Liguria-Hotels.html',
                    'country_name': '意大利'},
                   {'city_name': '拉斯佩齐亚',
                    'city_url': 'https://www.tripadvisor.cn/Tourism-g187824-La_Spezia_Province_of_La_Spezia_Liguria-Vacations.html',
                    'country_name': '意大利'},
                   {'city_name': '巴斯',
                    'city_url': 'https://www.tripadvisor.cn/Hotels-g187346-Wiesbaden_Hesse-Hotels.html',
                    'country_name': '英国'},
                   {'city_name': '阿维尼翁',
                    'city_url': 'https://www.tripadvisor.cn/Hotels-g187212-Avignon_Vaucluse_Provence_Alpes_Cote_d_Azur-Hotels.html',
                    'country_name': '法国'},
                   {'city_name': '苏格兰', 'city_url': 'https://www.tripadvisor.cn/Hotels-g186485-Scotland-Hotels.html',
                    'country_name': '英国'},
                   {'city_name': '牛津',
                    'city_url': 'https://www.tripadvisor.cn/Hotels-g186361-Oxford_Oxfordshire_England-Hotels.html',
                    'country_name': '英国'},
                   {'city_name': '托斯卡纳', 'city_url': 'https://www.tripadvisor.cn/Hotels-g187893-Tuscany-Hotels.html',
                    'country_name': '意大利'},
                   {'city_name': '米克诺斯',
                    'city_url': 'https://www.tripadvisor.cn/Hotels-g189430-Mykonos_Cyclades_South_Aegean-Hotels.html',
                    'country_name': '希腊'},
                   {'city_name': '剑桥',
                    'city_url': 'https://www.tripadvisor.cn/Hotels-g186225-Cambridge_Cambridgeshire_England-Hotels.html',
                    'country_name': '英国'},
                   # {'city_name': '采尔马特',
                   #  'city_url': 'https://www.tripadvisor.cn/Hotels-g188098-Zermatt_Canton_of_Valais_Swiss_Alps-Hotels.html',
                   #  'country_name': '瑞士'},
                   {'city_name': '阿维尼翁',
                    'city_url': 'https://www.tripadvisor.cn/Hotels-g187212-Avignon_Vaucluse_Provence_Alpes_Cote_d_Azur-Hotels.html',
                    'country_name': '法国'},

                   {'city_name': '毛里求斯',
                    'city_url': 'https://www.tripadvisor.cn/Hotels-g293816-Mauritius-Hotels.html',
                    'country_name': '毛里求斯'},
                   # {'city_name': '汤布院',
                   #  'city_url': 'https://www.tripadvisor.cn/Hotels-g503920-Tonbridge_Kent_England-Hotels.html',
                   #  'country_name': '日本'},
                   # {'city_name': '赛舌儿',
                   #  'city_url': 'https://www.tripadvisor.cn/Hotels-g187443-Seville_Province_of_Seville_Andalucia-Hotels.html',
                   #  'country_name': '赛舌儿'},
                   {'city_name': '函馆',
                    'city_url': 'https://www.tripadvisor.cn/Hotels-g298151-Hakodate_Hokkaido-Hotels.html',
                    'country_name': '日本'},
                   {'city_name': '卡萨布兰卡',
                    'city_url': 'https://www.tripadvisor.cn/Hotels-g293732-Casablanca_Grand_Casablanca_Region-Hotels.html',
                    'country_name': '摩洛哥'},
                   {'city_name': '马拉喀什',
                    'city_url': 'https://www.tripadvisor.cn/Hotels-g293734-Marrakech_Marrakech_Tensift_El_Haouz_Region-Hotels.html',
                    'country_name': '摩洛哥'},
                   {'city_name': '瓦尔扎扎特',
                    'city_url': 'https://www.tripadvisor.cn/Hotels-g304018-Ouarzazate_Souss_Massa_Draa_Region-Hotels.html',
                    'country_name': '摩洛哥'},
                   {'city_name': '舍夫沙万',
                    'city_url': 'https://www.tripadvisor.cn/Hotels-g304013-Chefchaouen_Tangier_Tetouan_Region-Hotels.html',
                    'country_name': '摩洛哥'},
                   {'city_name': '名古屋',
                    'city_url': 'https://www.tripadvisor.cn/Hotels-g298106-Nagoya_Aichi_Prefecture_Tokai_Chubu-Hotels.html',
                    'country_name': '日本'},
                   {'city_name': '轻井泽町',
                    'city_url': 'https://www.tripadvisor.cn/Hotels-g325581-Karuizawa_machi_Kitasaku_gun_Nagano_Prefecture_Koshinetsu_Chubu-Hotels.html',
                    'country_name': '日本'},

                   {'city_name': '清迈 ', 'city_url': 'https://www.tripadvisor.cn/Hotels-g293917-Chiang_Mai-Hotels.html',
                    'country_name': '泰国'},
                   {'city_name': '澳门', 'city_url': 'https://www.tripadvisor.cn/Hotels-g664891-Macau-Hotels.html',
                    'country_name': '中国'},
                   {'city_name': '伊豆',
                    'city_url': 'https://www.tripadvisor.cn/Hotels-g790340-Izu_Shizuoka_Prefecture_Tokai_Chubu-Hotels.html',
                    'country_name': '日本'},
                   {'city_name': '长滩岛',
                    'city_url': 'https://www.tripadvisor.cn/Hotels-g294260-Boracay_Malay_Aklan_Province_Panay_Island_Visayas-Hotels.html',
                    'country_name': '菲律宾'},
                   {'city_name': '苏梅岛',
                    'city_url': 'https://www.tripadvisor.cn/Hotels-g293918-Ko_Samui_Surat_Thani_Province-Hotels.html',
                    'country_name': '泰国'},
                   {'city_name': '非斯',
                    'city_url': 'https://www.tripadvisor.cn/Hotels-g293733-Fes_Fes_Boulemane_Region-Hotels.html',
                    'country_name': '摩洛哥'},
                   {'city_name': '马尔代夫',
                    'city_url': 'https://www.tripadvisor.cn/Hotels-g293953-Maldives-Hotels.html',
                    'country_name': '马尔代夫'},
                   {'city_name': '宿雾',
                    'city_url': 'https://www.tripadvisor.cn/Hotels-g294261-Cebu_Island_Visayas-Hotels.html',
                    'country_name': '菲律宾'},
                   {'city_name': '巴厘岛',
                    'city_url': 'https://www.tripadvisor.cn/Hotels-g294226-Bali-Hotels.html',
                    'country_name': '印度尼西亚'},
                   {'city_name': '美奈',
                    'city_url': 'https://www.tripadvisor.cn/Hotels-g1009804-Mui_Ne_Phan_Thiet_Binh_Thuan_Province-Hotels.html',
                    'country_name': '越南'},
                   {'city_name': '芭提雅',
                    'city_url': 'https://www.tripadvisor.cn/Hotels-g293919-Pattaya_Chonburi_Province-Hotels.html',
                    'country_name': '泰国'},
                   {'city_name': '香港',
                    'city_url': 'https://www.tripadvisor.cn/Hotels-g294217-Hong_Kong-Hotels.html',
                    'country_name': '中国'},
                   {'city_name': '台湾',
                    'city_url': 'https://www.tripadvisor.cn/Hotels-g293910-Taiwan-Hotels.html',
                    'country_name': '中国'},
                   {'city_name': '热海',
                    'city_url': 'https://www.tripadvisor.cn/Hotels-g298122-Atami_Shizuoka_Prefecture_Tokai_Chubu-Hotels.html',
                    'country_name': '日本'}]

# 西贡,托斯卡纳,赛舌儿,瓦尔扎扎特,采尔马特,汤布院,赛舌儿
