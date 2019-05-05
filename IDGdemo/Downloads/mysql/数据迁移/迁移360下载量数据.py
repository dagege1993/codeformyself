import pymssql

conn = pymssql.connect(host='192.168.0.11', user='hlz1', password='hlz123', database='appdown')
cursor = conn.cursor()
