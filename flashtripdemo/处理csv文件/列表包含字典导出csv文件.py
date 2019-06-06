import pandas as pd
from pymongo import MongoClient

ll = [{'city_name': '布达佩斯', 'country_name': '匈牙利', 'max_page_num': '当前最多酒店数93'},
      {'city_name': '圣托里尼', 'country_name': '希腊', 'max_page_num': '当前最多酒店数148'},
      {'city_name': '哥本哈根', 'country_name': '丹麦', 'max_page_num': '当前最多酒店数32'},
      {'city_name': '布鲁塞尔', 'country_name': '比利时', 'max_page_num': '当前最多酒店数53'},
      {'city_name': '拉孔达米讷', 'country_name': '摩纳哥', 'max_page_num': '当前最多酒店数0'},
      {'city_name': '扎金索斯', 'country_name': '希腊', 'max_page_num': '当前最多酒店数46'},
      {'city_name': '巴黎', 'country_name': '法国', 'max_page_num': '当前最多酒店数300'},
      {'city_name': '塞维利亚', 'country_name': '西班牙', 'max_page_num': '当前最多酒店数54'},
      {'city_name': '米兰', 'country_name': '意大利', 'max_page_num': '当前最多酒店数130'},
      {'city_name': '特罗姆瑟', 'country_name': '挪威', 'max_page_num': '当前最多酒店数2'},
      {'city_name': '维也纳', 'country_name': '奥地利', 'max_page_num': '当前最多酒店数146'},
      {'city_name': '罗马', 'country_name': '意大利', 'max_page_num': '当前最多酒店数263'},
      {'city_name': '鹿特丹', 'country_name': '荷兰', 'max_page_num': '当前最多酒店数18'},
      {'city_name': '斯德哥尔摩', 'country_name': '瑞典', 'max_page_num': '当前最多酒店数63'},
      {'city_name': '佛罗伦萨', 'country_name': '意大利', 'max_page_num': '当前最多酒店数119'},
      {'city_name': '戛纳', 'country_name': '法国', 'max_page_num': '当前最多酒店数39'},
      {'city_name': '卑尔根', 'country_name': '挪威', 'max_page_num': '当前最多酒店数12'},
      {'city_name': '卢塞恩', 'country_name': '瑞士', 'max_page_num': '当前最多酒店数20'},
      {'city_name': '苏黎世', 'country_name': '瑞士', 'max_page_num': '当前最多酒店数55'},
      {'city_name': '尼斯', 'country_name': '法国', 'max_page_num': '当前最多酒店数38'},
      {'city_name': '雷克雅未克', 'country_name': '冰岛', 'max_page_num': '当前最多酒店数26'},
      {'city_name': '马德里', 'country_name': '西班牙', 'max_page_num': '当前最多酒店数172'},
      {'city_name': '雅典', 'country_name': '希腊', 'max_page_num': '当前最多酒店数71'},
      {'city_name': '奥斯陆', 'country_name': '挪威', 'max_page_num': '当前最多酒店数28'},
      {'city_name': '萨尔茨堡', 'country_name': '奥地利', 'max_page_num': '当前最多酒店数43'},
      {'city_name': '威尼斯', 'country_name': '意大利', 'max_page_num': '当前最多酒店数98'},
      {'city_name': '布拉格', 'country_name': '捷克', 'max_page_num': '当前最多酒店数200'},
      {'city_name': '慕尼黑', 'country_name': '德国', 'max_page_num': '当前最多酒店数83'},
      {'city_name': '蒙特卡洛', 'country_name': '摩纳哥', 'max_page_num': '当前最多酒店数7'},
      {'city_name': '赫尔辛基', 'country_name': '芬兰', 'max_page_num': '当前最多酒店数33'},
      {'city_name': '因特拉肯', 'country_name': '瑞士', 'max_page_num': '当前最多酒店数11'},
      {'city_name': '日内瓦', 'country_name': '瑞士', 'max_page_num': '当前最多酒店数32'},
      {'city_name': '爱丁堡', 'country_name': '英国', 'max_page_num': '当前最多酒店数65'},
      {'city_name': '法兰克福', 'country_name': '德国', 'max_page_num': '当前最多酒店数55'},
      {'city_name': '巴塞罗那', 'country_name': '西班牙', 'max_page_num': '当前最多酒店数208'},
      {'city_name': '伦敦', 'country_name': '英国', 'max_page_num': '当前最多酒店数300'},
      {'city_name': '罗瓦涅米', 'country_name': '芬兰', 'max_page_num': '当前最多酒店数5'}
      ]

result = [{'city_name': '拉斯佩齐亚', 'country_name': '意大利', 'err_msg': '没有城市'},
          {'city_name': '牛津', 'country_name': '英国', 'err_msg': '没有城市'},
          {'city_name': '采尔马特', 'country_name': '瑞士', 'err_msg': '没有城市'},
          {'city_name': '阿维尼翁', 'country_name': '法国', 'err_msg': '没有城市'},
          {'city_name': '苏格兰高地', 'country_name': '英国', 'err_msg': '没有城市'},
          {'city_name': '巴斯', 'country_name': '英国', 'err_msg': '没有城市'},
          {'city_name': '五渔村', 'country_name': '意大利', 'err_msg': '没有城市'},
          {'city_name': '托斯卡纳', 'country_name': '意大利', 'err_msg': '没有城市'},
          {'city_name': '剑桥', 'country_name': '英国', 'err_msg': '没有城市'}]

client = MongoClient(host='172.16.4.110', port=27017)
db_auth = client.admin

db = client['scripture']['tripadvisor_lostdesc']

result_list = []
for l in ll:
    value_result = list(l.values())
    queryArgs = {'city_name': value_result[0], "lost_desc": ''}  # 城市名字并且不缺失的统计数据
    search_res = db.find(queryArgs).count()
    value_result.append(search_res)
    result_list.append([str(value).replace('当前最多酒店数', '') for value in value_result])
    print(result_list)

name_attribute = ['城市', '国家', '最大酒店数', '以获取最大酒店数']
writerCSV = pd.DataFrame(columns=name_attribute, data=result_list)
writerCSV.to_csv('./max_hotel_num_acquired2.csv', encoding='utf-8')
