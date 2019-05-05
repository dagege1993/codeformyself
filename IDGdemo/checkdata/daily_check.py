# encoding=utf8
import json
import time
import pymysql
import requests

check_dict_list = [
    {'company': '海底捞',
     'category': '日抓取数',
     'type': '总数',
     'database': 'hotpot',
     'table': 'SHOP_WAITE',
     'param': 'crawlTime'
     },
    {'company': '海底捞',
     'category': '门店数',
     'type': '总数',
     'database': 'hotpot',
     'table': 'SHOP_DETAIL',
     'param': 'crawlTime'
     },
    {'company': '星巴克',
     'category': '门店数',
     'type': '总数',
     'database': 'shops',
     'table': 'Starbucks',
     'param': 'crawlTime'
     },
    {'company': '永辉',
     'category': '门店数',
     'type': '总数',
     'database': 'shops',
     'table': 'YongHui',
     'param': 'crawlTime'
     },
    {'company': '瑞幸咖啡',
     'category': '门店数',
     'type': '总数',
     'database': 'shops',
     'table': 'Luckin',
     'param': 'crawlTime'
     },
    {'company': '英语流利说',
     'category': '课程数',
     'type': '课程总数',
     'database': 'fluent',
     'table': 'COURSE',
     'param': 'times'
     },
    {'company': '海底捞',
     'category': '菜单',
     'type': '总数',
     'database': 'hotpot',
     'table': 'SHOP_MENU',
     'param': 'crawlTime'
     },
    {'company': '西贝',
     'category': '菜单',
     'type': '总数',
     'database': 'xibei',
     'table': 'XIBEI_MENU',
     'param': 'crawlTime'
     },
    {'company': '西贝',
     'category': '等待人数',
     'type': '总数',
     'database': 'xibei',
     'table': 'XIBEI_WAITE',
     'param': 'crawlTime'
     },
    {'company': '便利蜂',
     'category': '全国门店数',
     'type': '总数',
     'database': 'shops',
     'table': 'BianLiFeng',
     'param': 'crawlTime'
     },

]


def send_data(payload):
    url = "http://192.168.103.19:9702/checkdata/data/updateSimple"
    headers = {
        'token': "AqZoNwiHXyff4ZDr409DF45EUg=JbJRUmC5eYAVB",
        'cache-control': "no-cache",
        'Postman-Token': "45536d49-4d8f-434c-8385-670af7ba07d9"
    }
    print(payload)
    response = requests.request("POST", url, data=payload, headers=headers)
    print(response.text)


# 获取当天日期的总数
def get_payload(check_dict):
    database = check_dict.get('database')
    table = check_dict.get('table')
    param = check_dict.get('param')
    db = pymysql.connect("192.168.103.31", "root", "adminadmin", database)
    cursor = db.cursor()
    inquery_sql = """select count(*) from %s where %s >= '%s' and  %s < '%s';""" % (
        table, param, today_times, param, tomorrow)
    print(inquery_sql)
    cursor.execute(inquery_sql)
    results = cursor.fetchone()
    result = results[0]
    return result


# 格式化参数
def format_payload(data_count, check_dict):
    payload = {'param': {'company': '流利说', 'category': '课程', 'start': '2019-01-13', 'end': '2019-09-01'},
               'data': [{'type': '课程数', 'dt': '2019-01-13', 'data': 75}
                        ]}
    # 参数处理
    company = check_dict.get('company')
    category = check_dict.get('category')
    type = check_dict.get('type')
    payload['param']['company'] = company
    payload['param']['start'] = today_times
    payload['param']['category'] = category
    data_dict = payload['data'][0]
    data_dict['type'] = type
    data_dict['dt'] = today_times
    data_dict['data'] = data_count
    # payload = json.dumps(payload, ensure_ascii=False)
    # print(payload)
    payload = json.dumps(payload)

    return payload


if __name__ == '__main__':
    import datetime

    today_time = time.localtime(time.time())
    today_times = time.strftime("%Y-%m-%d", today_time)
    today = datetime.date.today()
    tomorrow = today + datetime.timedelta(days=1)
    # print('日期%s' % today_times)
    print('日期%s' % today)
    for check_dict in check_dict_list:
        data_count = get_payload(check_dict)
        print('总数是%s' % data_count)
        # 格式化参数
        payload = format_payload(data_count, check_dict)
        # 发送数据
        send_data(payload)
