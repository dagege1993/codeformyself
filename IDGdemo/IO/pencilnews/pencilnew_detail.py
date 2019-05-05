import json
import pymysql
import requests
import scrapy

# from pencilnews.pencilnews_all import mains
from pencilnews.pencilnews_all_company_id import mains


def get_company_detail(company_id):
    url = "https://api.pencilnews.cn/project/detail"
    querystring = {"id": "fb8479c6ed6a2c15",
                   "sa-super-property": "%7B%22device_id%22%3A%221503446%22%2C%22screen_width%22%3A1920%2C%22screen_height%22%3A1080%7D"}
    querystring['id'] = company_id

    headers = {
        'accept': "application/json, text/javascript, */*; q=0.01",
        'accept-encoding': "gzip, deflate, br",
        'accept-language': "zh-CN,zh;q=0.9,en;q=0.8",
        'devicetoken': "jBeQdHyYzcY3DP7N7eyz7X6MwNBtf2R81543307255048",
        'origin': "https://www.pencilnews.cn",
        'referer': "https://www.pencilnews.cn/projectdetail/1fff8da65ec9cc0f?from=project_list",
        'token': "H2BCgs6LD7MoysIp8SlnJpelfyMpykbvCCfhqnfvsJ9UGTrEUZGHRPWgkgZ51Kif",
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36",
        'cache-control': "no-cache",
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    storage(response)


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
        sql = "UPDATE XINIU SET legal_name = '%s',legal_person= '%s',registered_capital= '%s',competing_product= '%s' WHERE company_name = '%s'" % (
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
    result_lists = mains()  # 手动去调一次这个接口,获取最新的接口

    for company_id in result_lists:
        get_company_detail(company_id)
