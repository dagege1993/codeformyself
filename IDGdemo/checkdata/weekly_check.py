# encoding=utf8
import json
import pymysql
import requests

check_dict_list = [
    {'company': '投融资信息',
     'category': '投融资数据',
     'type': '总数',
     'database': 'company',
     'table': 'unions1203',
     'param': 'insert_times'
     },
    # {'company': '下载量',
    #  'category': '腾讯',
    #  'type': '总数',
    #  'database': 'downloads',
    #  'table': 'ANDROID_QQ_APP_DAILY',
    #  'param': 'stat_dt'
    #  },
    # {'company': '下载量',
    #  'category': '360',
    #  'type': '总数',
    #  'database': 'downloads',
    #  'table': 'ANDROID_SAFE_APP_DAILY',
    #  'param': 'stat_dt'
    #  },
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
    inquery_sql = """select count(*) from %s where %s >= '%s' and  %s <= '%s';""" % (
        table, param, monday, param, today)
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
    company = check_dict.get('company')
    category = check_dict.get('category')
    type = check_dict.get('type')
    payload['param']['company'] = company
    payload['param']['category'] = category
    payload['param']['start'] = today
    data_dict = payload['data'][0]
    data_dict['type'] = type
    data_dict['dt'] = today
    data_dict['data'] = data_count
    # payload = json.dumps(payload, ensure_ascii=False)
    payload = json.dumps(payload)
    return payload


if __name__ == '__main__':
    import datetime
    # 自定义时间，转为日期格式
    today = "2019-02-10"
    today = datetime.datetime.strptime(today, "%Y-%m-%d")
    # today = datetime.date.today()
    monday = today - datetime.timedelta(days=6)
    # 时间格式化字符串
    today = today.strftime("%Y-%m-%d")
    monday = monday.strftime("%Y-%m-%d")
    print('日期%s' % today)
    for check_dict in check_dict_list:
        data_count = get_payload(check_dict)
        print('总数是%s' % data_count)
        payload = format_payload(data_count, check_dict)
        send_data(payload)
