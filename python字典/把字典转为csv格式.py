# encoding=utf8
category_dict = {
    '便捷生活': '便捷生活',
    '购物': '购物', '购物优惠': '购物',
    '视频': '视频', '影音视听': '视频',
    '理财': '理财', '金融理财': '理财',
    '社交': '社交', '通讯': '社交', '通讯社交': '社交',
    '运动健康': '运动健康',
    '旅游酒店': '旅游酒店',
    '教育学习': '教育学习',
    '音乐': '音乐',
    '实用工具': '工具', '微应用': '工具', '常用工具': '工具', '软件': '工具',
    '系统': '系统', '系统安全': '系统', '手机美化': '系统', '主题壁纸': '系统',
    '摄影': '摄影', '摄影摄像': '摄影',
    '出行': '出行', '交通导航': '出行',
    '阅读': '阅读', '新闻阅读': '阅读',
    '育儿母婴': '育儿母婴',
    '办公商务': '办公商务',
    '生活服务': '生活服务',

}
result = list(category_dict)
print(result)
k_v_list = []
k_v = []
for k, v in category_dict.items():
    print(k, v)
    k_v.append(k)
    k_v.append(v)
    k_v_list.append(k_v)
    k_v = []
import csv

print(k_v_list)
with open('country.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    for row in k_v_list:
        writer.writerow(row)
