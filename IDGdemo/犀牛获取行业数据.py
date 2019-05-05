import pymysql

db = pymysql.connect("192.168.103.31", "root", "adminadmin", "company")
cursor = db.cursor()
# sql = """select DISTINCT industry from PENCILENEW;"""
sql = """select DISTINCT industry from XINIU1203;"""
cursor.execute(sql)
results = cursor.fetchall()
industry_list = []
for result in results:
    datas = result[0]
    # print(datas.split(","))
    datas_list = datas.split(",")
    for data in datas_list:
        if len(data) <= 5:
            industry_list.append(data)
            industry_list = list(set(industry_list))
print(industry_list)




