import pymysql

red_vc = ["真格", "梅花", "九合", "险峰", "联想之星", "华创", "清流", "明势", "阿米巴", "青松", "洪泰", "紫辉",
          "红杉", "经纬", "晨兴", "创新工场", "金沙江", "联创策源", "软银", "顺为", "高榕", "红点", "贝塔斯曼", "光速", "北极光", "蓝驰", "DCM", "远璟",
          "Frees",
          "GGV", "启明", "成为", "华创", "源码", "今日资本", "戈壁", "愉悦", "君联", "祥峰",
          "达晨", "深创投", "东方富海", "创东方", "启迪", "天图", "九鼎", "同创伟业", "华映", "盘古创富",
          "H capital", "Hillhouse", "DST", "Tiger", "TPG", "华平", "中金", "中信产业基金", "新天域", "GIC", "淡马锡", "华人文化", "鼎晖",
          "霸菱", "云峰",
          "弘毅", "海通开元", "景林", "中国文化产业基金",
          "腾讯", "百度", "阿里", "小米", "360", "京东", "58", "美团", "昆仑万维", "携程", "易车"
          ]


# if '阿里巴巴' in red_vc:
#     print(111)


# for red in red_vc:
#     if red in '阿里巴巴':
#         print(111)


def get_red_agency():
    db = pymysql.connect("192.168.103.31", "root", "adminadmin", "company")
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    # SQL 插入语句
    sql = """SELECT * FROM XINIU1203  where  agency like "%真格%" or agency like "%梅花%" or agency like "%九合%" or agency like "%险峰%" or agency like "%联想之星%" or agency like "%华创%" or agency like "%清流%" or agency like "%明势%" or agency like "%阿米巴%" or agency like "%青松%" or agency like "%洪泰%" or agency like "%紫辉%" or agency like "%红杉%" or agency like "%经纬%" or agency like "%晨兴%" or agency like "%创新工场%" or agency like "%金沙江%" or agency like "%联创策源%" or agency like "%软银%" or agency like "%顺为%" or agency like "%高榕%" or agency like "%红点%" or agency like "%贝塔斯曼%" or agency like "%光速%" or agency like "%北极光%" or agency like "%蓝驰%" or agency like "%DCM%" or agency like "%远璟%" or agency like "%Frees%" or agency like "%GGV%" or agency like "%启明%" or agency like "%成为%" or agency like "%华创%" or agency like "%源码%" or agency like "%今日资本%" or agency like "%戈壁%" or agency like "%愉悦%" or agency like "%君联%" or agency like "%祥峰%" or agency like "%达晨%" or agency like "%深创投%" or agency like "%东方富海%" or agency like "%创东方%" or agency like "%启迪%" or agency like "%天图%" or agency like "%九鼎%" or agency like "%同创伟业%" or agency like "%华映%" or agency like "%盘古创富%" or agency like "%H capital%" or agency like "%Hillhouse%" or agency like "%DST%" or agency like "%Tiger%" or agency like "%TPG%" or agency like "%华平%" or agency like "%中金%" or agency like "%中信产业基金%" or agency like "%新天域%" or agency like "%GIC%" or agency like "%淡马锡%" or agency like "%华人文化%" or agency like "%鼎晖%" or agency like "%霸菱%" or agency like "%云峰%" or agency like "%弘毅%" or agency like "%海通开元%" or agency like "%景林%" or agency like "%中国文化产业基金%" or agency like "%腾讯%" or agency like "%百度%" or agency like "%阿里%" or agency like "%小米%" or agency like "%360%" or agency like "%京东%" or agency like "%58%" or agency like "%美团%" or agency like "%昆仑万维%" or agency like "%携程%" or agency like "%易车%" and DATE_FORMAT(finance_time,'%Y-%m-%d') >= '2018-10-01' and DATE_FORMAT(finance_time,'%Y-%m-%d') <= '2018-10-31';"""
    try:
        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
        # 使用 fetchone() 方法获取一条数据
        datas = cursor.fetchall()
        for data in datas:
            print(data[7])
    except Exception as e:
        # 如果发生错误则回滚
        print(e)


# get_red_agency()
