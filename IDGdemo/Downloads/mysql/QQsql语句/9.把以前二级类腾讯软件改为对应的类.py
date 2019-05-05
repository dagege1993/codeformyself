# encoding=utf8
import json
import time

import requests

requests.packages.urllib3.disable_warnings()  # 忽略警告


def serch(kw):
    url = "https://sj.qq.com/myapp/searchAjax.htm"

    querystring = {"kw": "QQ%E7%A9%BA%E9%97%B4", "pns": "", "sid": ""}
    querystring['kw'] = kw
    payload = ""
    headers = {
        'cache-control': "no-cache",
        'Postman-Token': "56de42bf-e225-4c50-877c-911fa7a9fe49"
    }

    response = requests.request("GET", url, data=payload, headers=headers, params=querystring, verify=False)

    # print(response.text)
    time.sleep(3)
    response_text = json.loads(response.text)
    obj = response_text.get('obj')
    appDetails = obj.get('appDetails')
    appDetail = appDetails[0]
    category_lv2 = appDetail.get('categoryName')
    appName = appDetail.get('appName')
    print(kw, appName, category_lv2)
    update_sql = '''update ANDROID_QQ_APP set category_lv2 ='%s' where app_name ='%s' ''' % (category_lv2, kw)
    cursor.execute(update_sql)


if __name__ == '__main__':
    import pymysql

    db = pymysql.connect("192.168.103.31", "root", "adminadmin", "downloads")
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    sql = """select   app_name   from ANDROID_QQ_APP WHERE category_lv2 = '全部' or category_lv2 = '腾讯软件'"""
    cursor.execute(sql)
    # 提交到数据库执行
    db.commit()
    results = cursor.fetchall()
    print(results)
    for data in results:
        kw = data[0]
        serch(kw)
