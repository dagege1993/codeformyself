# 打开文件
import os
import time

import pymysql
import xlrd as xlrd

success = 0
fail = 0
rootdir = r'C:\Users\Administrator.DESKTOP-DV7S27B\Desktop\IDGdemo\IO\IT橘子'
list = os.listdir(rootdir)  # 列出文件夹下所有的目录与文件
for i in range(0, len(list)):
    path = os.path.join(rootdir, list[i])
    if os.path.isfile(
            path) and path == r'C:\Users\Administrator.DESKTOP-DV7S27B\Desktop\IDGdemo\IO\IT橘子\2018年12月15日投融资信息.xlsx':  # #判断路径是否为文件
        print('当前打开的是', path)
        workbook = xlrd.open_workbook(path)
        # 获取所有sheet
        # print(workbook)
        print(workbook.sheet_names())
        # 根据sheet索引或者名称获取sheet内容
        sheet2 = workbook.sheet_by_index(0)  # sheet索引从0开始
        # sheet的名称，行数，列数
        print(sheet2.name, sheet2.nrows, sheet2.ncols)
        for i in range(1, sheet2.nrows):
            # 获取整行和整列的值（数组）
            rows = sheet2.row_values(i)  # 获取第四行内容
            finance_time = rows[0]  # 把融资时间格式化输出
            import time
            timeArray = time.strptime(finance_time, "%Y-%m-%d")
            finance_time = time.strftime("%Y-%m-%d", timeArray)
            # print(finance_time)
            company_name = rows[2]
            legal_name = rows[3]
            city = rows[4]
            industry = rows[5]
            finance = rows[6]
            money = rows[7]
            agency = rows[8]
            brief = rows[9]
            past_financing = rows[10]
            teams = rows[11]
            localtime = time.localtime(time.time())
            str_time = time.strftime("%Y-%m-%d", localtime)
            db = pymysql.connect("192.168.103.31", "root", "adminadmin", "company")
            # 使用 cursor() 方法创建一个游标对象 cursor
            cursor = db.cursor()
            # SQL 插入语句
            sql = """INSERT INTO ITORANGE(project_name,brief,industry,city,finance_time,finance,money,agency,legal_person,legal_name,registered_capital,competing_product,past_financing,teams,types,insert_times) VALUES ("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%d","%s")""" % (
                company_name, brief, industry, city, finance_time, finance, money, agency, '', legal_name, '', '',
                past_financing, teams, 2, str_time)
            try:
                # 执行sql语句
                cursor.execute(sql)
                # 提交到数据库执行
                db.commit()
                print('成功公司', company_name)
                success += 1
            except Exception as e:
                fail += 1
                print(e)
                # 如果发生错误则回滚
                db.rollback()
                # print(company_name, brief, industry, city, finance_time, finance, money, agency)

            db.close()
print('成功数', success)
print('失败数', fail)
