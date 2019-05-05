import json
import time
import pymysql
import requests
from multiprocessing import Pool

PAGES = 6
success = 0
fail = 0


def first_requests(page_num):
    url = "https://api.pencilnews.cn/pay-project/whole-network-list"
    querystring = {"page": "2",
                   "address": "北京,上海,广州,深圳,杭州,成都,武汉,南京,西安,长沙"}
    headers = {'cache-control': "no-cache"}
    querystring['page'] = page_num
    response = requests.request("GET", url, headers=headers, params=querystring)
    storage(response)


def storage(response):
    response_text = json.loads(response.text)
    if response_text.get('message') == 'SUCCESS':
        data = response_text.get('data')
        items = data.get('items')
        for item in items:
            finance_time = item.get('annouced_time')
            company_name = item.get('name')
            legal_name = ''
            city = ''
            industry = ','.join(item.get('industry'))
            finance = item.get('latest_round')
            money = item.get('money_raised')
            company_id = item.get('id')
            brief = item.get('introduce')
            past_financing = ''
            registered_capital = ''
            legal_person = ''
            competing_product = ''
            teams = item.get('bright_label_string')
            agency = teams
            localtime = time.localtime(time.time())
            str_time = time.strftime("%Y-%m-%d", localtime)
            db = pymysql.connect("192.168.103.31", "root", "adminadmin", "company")
            # 使用 cursor() 方法创建一个游标对象 cursor
            cursor = db.cursor()
            # SQL 插入语句
            sql = """INSERT ignore PENCILENEW(project_name,brief,industry,city,finance_time,finance,money,agency,legal_person,legal_name,registered_capital,competing_product,past_financing,teams,types,insert_times,company_id) VALUES ("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%d","%s","%s")""" % (
                company_name, brief, industry, city, finance_time, finance, money, agency, legal_person, legal_name,
                registered_capital, competing_product, past_financing, teams, 3, str_time, company_id)
            print(sql)
            try:
                # 执行sql语句
                cursor.execute(sql)
                # 提交到数据库执行
                db.commit()
                print('铅笔到插入数据项目名称', company_name)
                global success
                success += 1
            except Exception as e:
                # 如果发生错误则回滚
                print(e)
                global fail
                fail += 1
                db.rollback()
            db.close()


def mains(page_num):
    print('当前是第%s页' % page_num)
    first_requests(page_num)


# 多进程跑
if __name__ == '__main__':
    start_time = time.time()
    page_nums = []
    pool = Pool(processes=6)
    for page_num in range(1, PAGES + 1):
        page_nums.append(page_num)
    print(page_nums)
    pool.map(mains, page_nums)
    end_time = time.time()
    print('执行完成的时间%s', end_time - start_time)
