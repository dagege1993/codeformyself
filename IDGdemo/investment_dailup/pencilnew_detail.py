import json
import pymysql
import requests
import scrapy

COMPANY_ID_LIST = []


# 获取数据库十一月份公司名字
def get_company_name_list():
    company_name_list = []
    db = pymysql.connect('192.168.103.31', 'root', 'adminadmin', 'company')
    cursor = db.cursor()
    sql = """Select project_name From PENCILENEW Where DATE_FORMAT(finance_time,'%Y-%m-%d') >= '2018-10-01' and DATE_FORMAT(finance_time,'%Y-%m-%d') <= '2018-11-30' AND legal_name = '' ORDER BY finance_time;"""
    cursor.execute(sql)
    db.commit()
    datas = cursor.fetchall()
    for data in datas:
        company_name_list.append(''.join(data))
    return company_name_list


# 搜索公司名字获取公司ID
def first_requests(company_name):
    url = "https://api.pencilnews.cn/pay-project/search"
    querystring = {"page": "1", "keyword": "%E6%9C%A8%E6%A7%BF%E6%A0%A1%E5%9B%AD%20"}
    querystring['keyword'] = company_name
    payload = ""
    headers = {
        'cache-control': "no-cache",
    }

    response = requests.request("GET", url, data=payload, headers=headers, params=querystring)

    # print(response.text)
    response_text = json.loads(response.text)
    if response_text.get('message') == 'SUCCESS':
        data = response_text.get('data')
        item = data.get('res')[0]  # 一般来说搜索只有一个
        company_id = item.get('id')
        global COMPANY_ID_LIST
        COMPANY_ID_LIST.append(company_id)


def get_company_detail(company_id):
    url = "https://api.pencilnews.cn/project/detail"
    querystring = {"id": "fcec6f7cc5c240d6",
                   "sa-super-property": "%7B%22device_id%22%3A%221503446%22%2C%22screen_width%22%3A1920%2C%22screen_height%22%3A1080%7D"}
    querystring['id'] = company_id
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
    }
    response = requests.request("GET", url, data=payload, headers=headers, params=querystring)
    storage(response)  # 解析详情页数据


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
        # 还有一个字段在另外的接口,竞争对手
        url = "https://www.pencilnews.cn/projectdetail/" + project.get('id')
        querystring = {"from": "search_project_list"}
        headers = {'cache-control': "no-cache", }
        response = requests.request("GET", url, headers=headers, params=querystring)
        competing_product = scrapy.Selector(text=response.text)
        competing_product = competing_product.xpath('//*[@class="competitor-name"]//text()').extract()
        competing_product = ','.join([competing for competing in competing_product])
        db = pymysql.connect("192.168.103.31", "root", "adminadmin", "company")
        # 使用 cursor() 方法创建一个游标对象 cursor
        cursor = db.cursor()
        # SQL 插入语句
        sql = "UPDATE PENCILENEW SET legal_name = '%s',legal_person= '%s',registered_capital= '%s',competing_product= '%s' WHERE project_name = '%s'" % (
            legal_name, legal_person, registered_capital, competing_product, update_name)
        try:
            # 执行sql语句
            cursor.execute(sql)
            # 提交到数据库执行
            db.commit()
            print('修改后的项目名称', update_name)
        except:
            # 如果发生错误则回滚
            db.rollback()
        db.close()


if __name__ == '__main__':
    company_name_list = get_company_name_list()  # 获取数据库11月份公司名字
    print(company_name_list)
    for company_name in company_name_list:
        first_requests(company_name)
    print(COMPANY_ID_LIST)
    for company_id in list(set(COMPANY_ID_LIST)):
        print(company_id)
        get_company_detail(company_id)
