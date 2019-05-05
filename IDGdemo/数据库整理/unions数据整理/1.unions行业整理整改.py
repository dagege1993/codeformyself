# encoding=utf8
import pymysql
import xlrd

industrys_list = []
IDGIndustry = {}
path = r'C:\Users\Administrator.DESKTOP-DV7S27B\Desktop\需要维护的数据\行业分类.xlsx'
workbook = xlrd.open_workbook(path)
print(workbook)
print(workbook.sheet_names())
sheet2 = workbook.sheet_by_index(0)  # sheet索引从0开始
print(sheet2.name, sheet2.nrows, sheet2.ncols)
# 生成一个IDG行业的键值对
for i in range(1, sheet2.nrows):
    # 获取整行和整列的值（数组）
    rows = sheet2.row_values(i)  # 获取第四行内容
    # if 'IT橘子' in rows:
    #     print(rows)
    IDGIndustry[rows[1]] = rows[2]
print(IDGIndustry)
db = pymysql.connect("192.168.103.31", "root", "adminadmin", "company")
# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()
# SQL 插入语句
# sql = """select project_name, industry  from unions1203  where types = 2  and DATE_FORMAT(insert_times,'%Y-%m-%d') <= '2019-01-03'"""
sql = """select project_name, industry,types  from unions1203  where industry !=''  """

# 执行sql语句
cursor.execute(sql)
# 提交到数据库执行
db.commit()
datas = cursor.fetchall()
for data in datas:
    project_name = data[0]
    industry = data[1]
    types = data[2]
    IDG_industry = IDGIndustry.get(industry)
    # print(project_name, industry, IDG_industry)
    if IDG_industry and project_name and industry:
        # pass
        new_sql = "UPDATE unions1203 SET IDG_industry = '%s' WHERE project_name = '%s'" % (IDG_industry, project_name)
        try:
            pass
            # 执行sql语句
            cursor.execute(new_sql)
            # 提交到数据库执行
            db.commit()
            # print(data)
        except Exception as e:
            print(e)
            # 如果发生错误则回滚
            db.rollback()
    else:
        print(project_name, industry, IDG_industry, types)
        # print(industry)
        industry_list = industry.split(',')
        for industry in industry_list:
            industrys_list.append(industry)
print(industrys_list)
from collections import Counter

print(Counter(industrys_list))
