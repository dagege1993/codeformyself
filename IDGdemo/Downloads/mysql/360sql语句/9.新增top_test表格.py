



import pymysql

db = pymysql.connect("192.168.103.31", "root", "adminadmin", "downloads")

# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()

# 使用预处理语句创建表
sql = """

CREATE TABLE `ANDROID_SAFE_APP_TOP_TEST3` (
  `log_id` bigint(20) NOT NULL,
  `stat_dt` date NOT NULL,
  `source` varchar(30) NOT NULL,
  `cate` varchar(60) NOT NULL,
  `sort` varchar(60) NOT NULL,
  `sub` varchar(60) NOT NULL,
  `app_id` bigint(20) NOT NULL,
  `app_name` varchar(120) NOT NULL,
  `app_keys` varchar(30) NOT NULL,
  `downs` bigint(20) NOT NULL,
  `top_num` int(11) NOT NULL,
  `dt_type` varchar(30) NOT NULL,
  `page_num` varchar(30) NOT NULL,
  `category_lv3` varchar(60) DEFAULT NULL
) ;

"""
cursor.execute(sql)
# 提交到数据库执行
db.commit()

# 关闭数据库连接
db.close()
