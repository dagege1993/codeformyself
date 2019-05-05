# encoding=utf-8
import json
import pymysql
import requests
import scrapy
from multiprocessing import Pool


def get_company_detail(company_id):
    url = "https://api.pencilnews.cn/project/detail"

    querystring = {"id": "77cd43bb6b8b71b6",
                   "sa-super-property": "%7B%22device_id%22%3A%221503446%22%2C%22screen_width%22%3A1920%2C%22screen_height%22%3A1080%7D"}
    querystring['id'] = company_id
    # querystring['id'] = '77cd43bb6b8b71b6'
    payload = ""
    headers = {
        'Host': "api.pencilnews.cn",
        'Connection': "keep-alive",
        'Accept': "application/json, text/javascript, */*; q=0.01",
        'Origin': "https://www.pencilnews.cn",
        'devicetoken': "fcFDdEZYypGPbmkwmAG7PtR8D8XSxsWP1543983687073",
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36",
        'token': "dB4QIP05lIlkbPeAQbuxAleSBcO7c91rMNXdIOSX0312-64KP1am06_G9vf_KfCv",
        'Referer': "https://www.pencilnews.cn/projectdetail/fcec6f7cc5c240d6?from=new_project_list",
        'Accept-Encoding': "gzip, deflate, br",
        'Accept-Language': "zh-CN,zh;q=0.9,en;q=0.8",
        'cache-control': "no-cache",
        'Postman-Token': "d9191f3a-1d39-4578-bab8-6e51c8918092"
    }

    response = requests.request("GET", url, data=payload, headers=headers, params=querystring)

    print(response.text)
    storage(response)


# 储存铅笔道公司详情页数据
def storage(response):
    response_text = json.loads(response.text)
    if response_text.get('message') == 'SUCCESS':
        data = response_text.get('data').get('content')
        project = data.get('project')
        business = data.get('business')
        # 查询的名字
        update_name = project.get('name')
        # 这里是新增的字段
        legal_name = business.get('name')
        legal_person = business.get('opername')
        registered_capital = business.get('registcapi')
        # 还有一个字段在另外的接口
        url = "https://www.pencilnews.cn/projectdetail/" + project.get('id')
        querystring = {"from": "search_project_list"}
        headers = {'cache-control': "no-cache", }
        response = requests.request("GET", url, headers=headers, params=querystring)
        competing_product = scrapy.Selector(text=response.text)
        competing_product = competing_product.xpath('//*[@class="competitor-name"]//text()').extract()
        competing_product = ','.join([competing for competing in competing_product])
        # print(competing_product)
        db = pymysql.connect("192.168.103.31", "root", "adminadmin", "company")
        # 使用 cursor() 方法创建一个游标对象 cursor
        cursor = db.cursor()
        # SQL 插入语句
        sql = "UPDATE PENCILENEW SET legal_name = '%s',legal_person= '%s',registered_capital= '%s',competing_product= '%s' WHERE project_name = '%s'" % (
            legal_name, legal_person, registered_capital, competing_product, update_name)
        try:
            # 执行sql语句
            print(sql)
            cursor.execute(sql)
            # 提交到数据库执行
            db.commit()
            print('修改后的项目名称', update_name)
        except:
            # 如果发生错误则回滚
            db.rollback()
        db.close()


# 查询一段时间内的公司Id
def get_recent_company_id():
    db = pymysql.connect("192.168.103.31", "root", "adminadmin", "company")
    cursor = db.cursor()
    company_id_list = []
    inqury_sql = """select company_id from PENCILENEW WHERE DATE_FORMAT(finance_time,'%Y-%m-%d') >= '2018-11-01' and  DATE_FORMAT(finance_time,'%Y-%m-%d') <= '2019-01-11'"""
    cursor.execute(inqury_sql)
    results = cursor.fetchall()
    for result in results:
        result = result[0]
        company_id_list.append(result)
    return company_id_list


if __name__ == '__main__':
    company_id_list = get_recent_company_id()
    print(company_id_list)
    pool = Pool(processes=6)
    pool.map(get_company_detail, company_id_list)
    # for company_id in company_id_list:
    #     get_company_detail(company_id)
