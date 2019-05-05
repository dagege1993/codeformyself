# -*- coding: UTF-8 -*-
import os
import time
import pymysql
import scrapy

from twisted_IO import mains

sql_list = []
start_time = time.time()
# root_dir = r'C:\Users\Administrator.DESKTOP-DV7S27B\Desktop\IO\行业复测'
root_dir = r'C:\Users\Administrator.DESKTOP-DV7S27B\Desktop\IO\bymyself'
# root_dir = r'C:\Users\Administrator.DESKTOP-DV7S27B\Desktop\IO\selenium公司抓取'
lists = os.listdir(root_dir)  # 列出文件夹下所有的目录与文件
for i in range(0, len(lists)):
    path = os.path.join(root_dir, lists[i])
    if os.path.isfile(path):  # #判断路径是否为文件
        with open(path, 'r', encoding='utf-8') as f:  # 要读取非UTF-8编码的文本文件，需要给open()函数传入encoding参数
            page_source = f.read()
            page_sel = scrapy.Selector(text=page_source)
            # result = page_sel.xpath('//*[@class="jsx-732187119 table-section"]')
            # result = page_sel.xpath('//*[@class="jsx-732187119 table-body"]')
            result = page_sel.xpath('//*[@class="jsx-2833694364 table-section"]')
            # print('打印第一次解析的结果', result)
            for i in result:
                # print(i.extract())
                page_sel = scrapy.Selector(text=i.extract())
                name = page_sel.xpath('/html/body/div/div/div[1]/div/div[2]/div[1]/a/text()').extract_first()  # 公司名
                brief = page_sel.xpath('/html/body/div/div/div[1]/div/div[2]/div[2]/text()').extract_first()  # 简介
                industry = page_sel.xpath('/html/body/div/div/div[2]/span//text()').extract_first()  # 行业
                city = page_sel.xpath('/html/body/div/div/div[3]/text()').extract_first()  # 城市
                times = page_sel.xpath('/html/body/div/div/div[4]/text()').extract_first()  # 融资时间
                finance = page_sel.xpath('/html/body/div/div/div[5]/text()').extract_first()  # 融资时间
                money = page_sel.xpath('/html/body/div/div/div[6]/text()').extract_first()  # 融资金额
                agencys = page_sel.xpath('/html/body/div/div/div[7]/div//text()').extract()  # 融资机构
                agency = ''.join([agency for agency in agencys])
                localtime = time.localtime(time.time())
                str_time = time.strftime("%Y-%m-%d", localtime)
                db = pymysql.connect("192.168.103.31", "root", "adminadmin", "company")
                # print(name, brief, industry, city, times, finance, money, agency)
                # 使用 cursor() 方法创建一个游标对象 cursor
                cursor = db.cursor()
                # SQL 插入语句
                sql = """INSERT INTO XINIU1203(project_name,brief,industry,city,finance_time,finance,money,agency,legal_person,legal_name,registered_capital,competing_product,past_financing,teams,types,insert_times) VALUES ("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%d","%s")""" % (
                    name, brief, industry, city, times, finance, money, agency, '', '', '', '', '', '', 1, str_time)
                try:
                    # 执行sql语句
                    cursor.execute(sql)
                    # 提交到数据库执行
                    db.commit()
                except Exception as e:
                    print(e)
                    # 如果发生错误则回滚
                    db.rollback()
                    print(name, brief, industry, city, times, finance, money, agency)

                db.close()
end_time = time.time()
print('花费时间', end_time - start_time)
