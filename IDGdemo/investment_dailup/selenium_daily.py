# coding = utf-8
import os
import time

import pymysql
import scrapy

from selenium import webdriver


def seleniums():
    # 为了selenium加上代理先
    chromeOptions = webdriver.ChromeOptions()
    # chromeOptions.add_argument('--headless')  # 设置无头浏览器,节约内存
    browser = webdriver.Chrome(chrome_options=chromeOptions)
    browser.get("http://www.xiniudata.com/project/lib")
    browser.maximize_window()
    for i in range(2):
        try:
            js = "var q=document.documentElement.scrollTop=100000"
            browser.execute_script(js)
            time.sleep(1)
        except:
            pass
    # browser.find_element_by_link_text('登录网站').click()  # 点击登录按钮
    time.sleep(6)
    for i in range(5):
        try:
            # 将滚动条移动到页面的底部
            js = "var q=document.documentElement.scrollTop=100000"
            browser.execute_script(js)
            time.sleep(3)
        except:
            pass
    localtime = time.localtime(time.time())
    str_time = time.strftime("%Y-%m-%d", localtime)
    file_path = r'C:\Users\Administrator.DESKTOP-DV7S27B\Desktop\IDGdemo\investment_dailup\犀牛数据列表页' + '\\' + str_time + ".html"
    print(file_path)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(browser.page_source)
    browser.quit()


def storage():
    localtime = time.localtime(time.time())
    str_time = time.strftime("%Y-%m-%d", localtime)  # 获取当前时间
    # str_time = '2018-12-28'
    root_dir = r'C:\Users\Administrator.DESKTOP-DV7S27B\Desktop\IDGdemo\investment_dailup\犀牛数据列表页'
    lists = os.listdir(root_dir)  # 列出文件夹下所有的目录与文件
    for i in range(0, len(lists)):
        path = os.path.join(root_dir, lists[i])
        if os.path.isfile(path) and str_time in path:  # #判断路径是否为文件,而且只有今天的才让继续走,以前的入过了就不管了
            with open(path, 'r', encoding='utf-8') as f:  # 要读取非UTF-8编码的文本文件，需要给open()函数传入encoding参数
                page_source = f.read()
                page_sel = scrapy.Selector(text=page_source)
                result = page_sel.xpath('//*[@class="jsx-2833694364 table-section"]')
                for i in result:
                    # print(i.extract())
                    page_sel = scrapy.Selector(text=i.extract())
                    name = page_sel.xpath('//*[@class="jsx-1418988208 name-link"]/text()').extract_first()  # 公司名
                    name = name.strip()  # 去掉项目名称两边的空格
                    brief = page_sel.xpath('//*[@class="jsx-1418988208 brief"]/text()').extract_first()  # 简介
                    industry = ','.join(page_sel.xpath('/html/body/div/div/div[2]//text()').extract())  # 行业
                    city = page_sel.xpath('/html/body/div/div/div[3]/text()').extract_first()  # 城市
                    times = page_sel.xpath('/html/body/div/div/div[4]/text()').extract_first()  # 融资时间
                    finance = page_sel.xpath('/html/body/div/div/div[5]/text()').extract_first()  # 融资时间
                    money = page_sel.xpath('/html/body/div/div/div[6]/text()').extract_first()  # 融资金额
                    agency = ''.join(page_sel.xpath('/html/body/div/div/div[7]//text()').extract())  # 投资机构
                    localtime = time.localtime(time.time())
                    str_time = time.strftime("%Y-%m-%d", localtime)
                    db = pymysql.connect("192.168.103.31", "root", "adminadmin", "company")
                    # 使用 cursor() 方法创建一个游标对象 cursor
                    cursor = db.cursor()
                    # SQL 插入语句
                    sql = """INSERT INTO XINIU1203(project_name,brief,industry,city,finance_time,finance,money,agency,legal_person,legal_name,registered_capital,competing_product,past_financing,teams,types,insert_times) VALUES ("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%d","%s")""" % (
                        name, brief, industry, city, times, finance, money, agency, '', '', '', '', '', '', 1, str_time)
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
                        print(name, brief, industry, city, times, finance, money, agency)

                    db.close()


def main_progress():
    try:
        seleniums()  # 每天跑一遍
        storage()  # 存储  ,存储是按照每天项目名称和融资时间去重,存是存到犀牛自己表中
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main_progress()
