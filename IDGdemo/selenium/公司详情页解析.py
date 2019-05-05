# -*- coding: UTF-8 -*-
import os
import time
import pymysql
import scrapy

sql_list = []
start_time = time.time()

root_dir = r'C:\Users\Administrator.DESKTOP-DV7S27B\Desktop\IDGdemo\selenium\selenium公司详情'
lists = os.listdir(root_dir)  # 列出文件夹下所有的目录与文件
for i in range(0, len(lists)):
    path = os.path.join(root_dir, lists[i])
    if os.path.isfile(path):  # #判断路径是否为文件
        with open(path, 'r', encoding='utf-8') as f:  # 要读取非UTF-8编码的文本文件，需要给open()函数传入encoding参数
            page_source = f.read()
            page_sel = scrapy.Selector(text=page_source)
            name = page_sel.xpath('//*[@id="header"]/div[2]/div[1]/span[1]//text()').extract_first()
            # 这里是新增的字段
            legal_name = page_sel.xpath('//*[@id="gongshangInfo"]/div[3]/div[1]/span[2]/text()').extract_first()
            legal_person = page_sel.xpath('//*[@id="gongshangInfo"]/div[3]/div[2]/span[2]/text()').extract_first()
            registered_capital = page_sel.xpath(
                '//*[@id="gongshangInfo"]/div[3]/div[4]/table/tbody/tr/td[3]//text()').extract()
            registered_capital = list(set(registered_capital))  # 为了去重重复的'-'元素
            for capital in registered_capital:
                if '-' == capital:
                    registered_capital.remove(capital)  # 列表按值去掉元素
            print(name, registered_capital)
            registered_capital = sum([float(capital.replace('万人民币', '').strip()) for capital in registered_capital])
            competing_products = page_sel.xpath('//*[@class="jsx-2833694364 table-section"]')  # 取第二个
            for product in competing_products:
                print(product.extract())
                product_source = scrapy.Selector(text=product.extract())
                # competing_product = product_source.xpath('/html/body/div/div/div[4]/span/span/span[1]/a//text()').extract_first()
                competing_product = product_source.xpath('/html/body/div/div/div[1]/div/div[2]/div[1]/a//text()').extract_first()
                if competing_product:
                    competing_product_list = ''.join(competing_product)
            db = pymysql.connect("192.168.103.31", "root", "adminadmin", "company")
            # 使用 cursor() 方法创建一个游标对象 cursor
            cursor = db.cursor()
            # SQL 插入语句
            sql = "UPDATE XINIU1203 SET legal_name = '%s',legal_person= '%s',registered_capital= '%s',competing_product= '%s' WHERE project_name = '%s'" % (
                legal_name, legal_person, registered_capital, competing_product_list, name)
            print(sql)
            try:
                # 执行sql语句
                cursor.execute(sql)
                # 提交到数据库执行
                db.commit()
            except Exception as e:
                print(e)
                # 如果发生错误则回滚
                db.rollback()
            db.close()
end_time = time.time()
print('花费时间', end_time - start_time)
