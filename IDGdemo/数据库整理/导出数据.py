import pymysql

db = pymysql.connect("192.168.103.31", "root", "adminadmin", "downloads")

# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()

path = r'C:\Users\Administrator.DESKTOP-DV7S27B\Desktop\ANDROID_SAFE_APP_TOP.sql'
with open(path, 'r', encoding='utf8') as file:
    for line in file:
        data = file.readline()
        if data != 'GO\n' and data.startswith('INSERT'):
            data = data.replace('[', '')
            data = data.replace(']', '')
            data = data.replace('dbo.', '')
            data = data.replace('N', '')
            data = data.replace('ISERT', 'INSERT')
            print(data)
            cursor.execute(data)
            # 提交到数据库执行
            db.commit()
    # 关闭数据库连接
    db.close()
