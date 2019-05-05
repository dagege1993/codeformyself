# encoding=utf8
import json
import pandas as pd
import time
import pymysql
import requests

check_dict_list = [
    {'company': '海底捞',
     'category': '排队人数',
     'type': '总数',
     'database': 'hotpot',
     'table': 'SHOP_WAITE',
     'param': 'crawlTime',
     'group_param': 'typeName',
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
    group_param = check_dict.get('group_param')
    db = pymysql.connect("192.168.103.31", "root", "adminadmin", database)
    cursor = db.cursor()
    # inquery_sql = """select count(*) from %s where %s >= '%s' and  %s < '%s';""" % (table, param, today_times, param, tomorrow)
    inquery_sql = """select typeName,sum(waitNum) from %s    where %s >= '%s' and  %s < '%s' GROUP BY %s;""" % (
        table, param, today_times, param, tomorrow, group_param)
    print(inquery_sql)
    cursor.execute(inquery_sql)
    results = cursor.fetchall()
    df_data = pd.DataFrame(list(results))  # 转换成DataFrame格式
    print(df_data)

    name_list = df_data[0].tolist()
    value_list = df_data[1].tolist()
    print(name_list)
    print(value_list)
    df_dict = dict(zip(name_list, value_list))
    return df_dict


# 格式化参数
def format_payload(data_dict, check_dict):
    payload = {'param': {'company': '流利说', 'category': '课程', 'start': '2019-01-13', 'end': '2019-09-01'},
               'data': [{'type': '课程数', 'dt': '2019-01-13', 'data': 75}]
               }
    # 参数处理
    company = check_dict.get('company')
    category = check_dict.get('category')
    type = check_dict.get('type')
    payload['param']['company'] = company
    payload['param']['start'] = today_times
    payload['param']['category'] = category
    data = []
    for keys, value in data_dict.items():
        post_dict = {}
        post_dict['type'] = keys
        post_dict['data'] = str(value)
        post_dict['dt'] = today_times
        data.append(post_dict)
    payload['data'] = data
    print(data)
    print('上传的参数', payload)
    # payload = json.dumps(payload, ensure_ascii=False)
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
        data_dict = get_payload(check_dict)
        print('总数是%s' % data_dict)
        # 格式化参数
        payload = format_payload(data_dict, check_dict)
        # 发送数据
        send_data(payload)
