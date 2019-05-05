import pymysql
import pandas as pd

db = pymysql.connect("192.168.103.31", "root", "adminadmin", "downloads")

path = r'C:\Users\Administrator.DESKTOP-DV7S27B\Desktop\需要维护的数据\下载量\下载量二级类和对应的种类.xlsx'
data_excel = pd.read_excel(path)
print(data_excel)
lv2 = data_excel['二级类']
category = data_excel['种类']
category_dict = dict(zip(lv2, category))
print(category_dict)
cursor = db.cursor()
for lv2, category in category_dict.items():
    # print(result)
    sql = """UPDATE ANDROID_SAFE_APP SET category = '%s' WHERE category_lv2 = '%s'""" % (category, lv2)
    print(sql)
    # cursor.execute(sql)
    # 提交到数据库执行
    db.commit()
print(category_dict)
{'便捷生活': '便捷生活', '购物': '购物', '购物优惠': '购物', '视频': '视频', '影音视听': '视频', '理财': '理财', '金融理财': '理财', '社交': '社交', '通讯': '社交',
 '通讯社交': '社交', '运动健康': '运动健康', '旅游酒店': '旅游酒店', '教育学习': '教育学习', '音乐': '音乐', '实用工具': '工具', '微应用': '工具', '常用工具': '工具',
 '软件': '工具', '系统': '系统', '系统安全': '系统', '手机美化': '系统', '主题壁纸': '系统', '摄影': '摄影', '摄影摄像': '摄影', '出行': '出行', '交通导航': '出行',
 '阅读': '阅读', '新闻阅读': '阅读', '育儿母婴': '育儿母婴', '办公商务': '办公商务', '生活服务': '生活服务'}
