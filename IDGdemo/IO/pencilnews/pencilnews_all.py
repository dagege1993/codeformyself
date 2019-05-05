import json
import time

import pymysql
import requests

PAGES = 552


def first_requests(page_num):
    url = "https://api.pencilnews.cn/pay-project/list"
    querystring = {"page": "1"}
    payload = ""
    headers = {
        'cache-control': "no-cache",
    }
    querystring['page'] = page_num
    response = requests.request("GET", url, data=payload, headers=headers, params=querystring)
    storage(response)


def storage(response):
    response_text = json.loads(response.text)
    if response_text.get('message') == 'SUCCESS':
        data = response_text.get('data')
        items = data.get('items')
        for item in items:
            finance_time = item.get('publish_time').split(' ')[0]
            company_name = item.get('name')
            legal_name = ''
            city = item.get('office_address')
            industry = ','.join(item.get('industry'))
            finance = item.get('stage_name')
            money = item.get('finance_money_origin')
            agency = ''
            brief = item.get('introduce')
            past_financing = ''
            registered_capital = ''
            legal_person = ''
            competing_product = ''
            teams = item.get('bright_label_string')
            localtime = time.localtime(time.time())
            str_time = time.strftime("%Y-%m-%d", localtime)
            db = pymysql.connect("192.168.103.31", "root", "adminadmin", "company")
            # 使用 cursor() 方法创建一个游标对象 cursor
            cursor = db.cursor()
            # SQL 插入语句
            sql = """INSERT INTO XINIU1129(project_name,brief,industry,city,finance_time,finance,money,agency,legal_person,legal_name,registered_capital,competing_product,past_financing,teams,types,insert_times) VALUES ("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%d","%s")""" % (
                company_name, brief, industry, city, finance_time, finance, money, agency, legal_person, legal_name,
                registered_capital, competing_product, past_financing, teams, 3, str_time)

            try:
                # 执行sql语句
                cursor.execute(sql)
                # 提交到数据库执行
                db.commit()
                print('铅笔到插入数据项目名称', company_name)
            except:
                # 如果发生错误则回滚
                db.rollback()

            db.close()


def mains():
    global PAGES
    for page_num in range(1, PAGES + 1):
        print('当前是第%s页' % page_num)
        first_requests(page_num)


if __name__ == '__main__':
    print(mains())
