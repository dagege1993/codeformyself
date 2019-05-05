import json
import time

import pymysql
import requests


def get_company_name_list():
    company_name_list = []
    db = pymysql.connect('192.168.103.31', 'root', 'adminadmin', 'company')
    cursor = db.cursor()
    sql = """Select project_name From PENCILENEW Where DATE_FORMAT(finance_time,'%Y-%m-%d') >= '2018-11-01' and DATE_FORMAT(finance_time,'%Y-%m-%d') <= '2018-11-30' AND legal_name = '' ORDER BY finance_time;"""
    cursor.execute(sql)
    db.commit()
    datas = cursor.fetchall()
    for data in datas:
        company_name_list.append(''.join(data))
    return company_name_list


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
            industry = ''.join(item.get('industry'))
            finance = item.get('stage_name')
            money = item.get('finance_money_origin')
            agency = item.get('bright_label_string')
            brief = item.get('introduce')
            past_financing = ''
            teams = item.get('bright_label_string')
            localtime = time.localtime(time.time())
            str_time = time.strftime("%Y-%m-%d", localtime)
            db = pymysql.connect("192.168.103.31", "root", "adminadmin", "company")
            # 使用 cursor() 方法创建一个游标对象 cursor
            cursor = db.cursor()
            # SQL 插入语句
            sql = """INSERT INTO XINIU(company_name,brief,industry,city,finance_time,finance,money,agency,insert_times,past_financing,teams,legal_name) VALUES ("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")""" % (
                company_name, brief, industry, city, finance_time, finance, money, agency, str_time, past_financing,
                teams, legal_name)

            try:
                # 执行sql语句
                cursor.execute(sql)
                # 提交到数据库执行
                db.commit()
                print('做了公司名和第几轮唯一索引后的插入数据', company_name)
            except:
                # 如果发生错误则回滚
                db.rollback()
                # print(company_name, brief, industry, city, finance_time, finance, money, agency)

            db.close()


if __name__ == '__main__':
    result_lists = get_company_name_list()
    print(result_lists)
    first_requests(1)
