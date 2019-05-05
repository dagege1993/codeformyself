# SELECT * FROM
# unions
# where
# agency
# like
# "%阿里%" or agency
# like
# "%百度%";
import datetime

sql_test = ["真格", "梅花", "九合", "险峰", "联想之星", "华创", "清流", "明势", "阿米巴", "青松", "洪泰", "紫辉",
            "红杉", "经纬", "晨兴", "创新工场", "金沙江", "联创策源", "软银", "顺为", "高榕", "红点", "贝塔斯曼", "光速", "北极光", "蓝驰", "DCM", "远璟",
            "Frees",
            "GGV", "启明", "成为", "华创", "源码", "今日资本", "戈壁", "愉悦", "君联", "祥峰",
            "达晨", "深创投", "东方富海", "创东方", "启迪", "天图", "九鼎", "同创伟业", "华映", "盘古创富",
            "H capital", "Hillhouse", "DST", "Tiger", "TPG", "华平", "中金", "中信产业基金", "新天域", "GIC", "淡马锡", "华人文化", "鼎晖",
            "霸菱", "云峰",
            "弘毅", "海通开元", "景林", "中国文化产业基金",
            "腾讯", "百度", "阿里", "小米", "360", "京东", "58", "美团", "昆仑万维", "携程", "易车"
            ]

# strs = "SELECT * FROM unions  where agency like"
# for te in sql_test:
#     strs = strs + ' ' + '"%' + te + '%"' + ' ' + 'or' + ' ' + 'agency like'
# print(strs)

data = ('放学嗨 ', '嘻哈文化IP服务提供商', '文化娱乐', '上海', '2018-10-01', 'Pre-A轮', '数千万人民币', '华映资本', '', '', '', '', '', '', 1,
        datetime.date(2018, 12, 3))
# print(list(data))
# results = list(data)
# results.append(1)
# print(results)

results = list(data)
results.append(1)
data_tuple = tuple(results)
print(data_tuple)
