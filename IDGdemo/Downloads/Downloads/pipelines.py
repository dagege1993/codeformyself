# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
import pymysql
from scrapy.conf import settings
from Downloads.settings import *


class DownloadsPipeline(object):
    def process_item(self, item, spider):
        return item


class MongodbPipeline(object):
    def __init__(self):
        host = settings['MONGODB_HOST']
        port = settings['MONGODB_PORT']
        dbname = settings['MONGODB_DBNAME']  # 数据库名
        client = pymongo.MongoClient(host=host, port=port)
        tdb = client[dbname]
        self.port = tdb[settings['MONGODB_DOCNAME']]  # 表名

    def process_item(self, item, spider):
        agentinfo = dict(item)

        self.port.insert(agentinfo)
        return item


class MysqlPipeline(object):
    # 采用同步的机制写入mysql
    def __init__(self):
        self.conn = pymysql.connect(MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DBNAME, charset="utf8",
                                    use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        insert_sql = """INSERT INTO 360_downloads2(app_names,
                   software, downloads_nums, types,crawl_time,id,pkgname,versionname)
                VALUES  ("%s","%d","%d","%s","%s","%d","%s","%s")""" % (
            item["name"], item["software"], item["downloads_nums"], item["types"], item["crawl_time"], item["id"],
            item["pkgname"], item["versionname"])
        # print(insert_sql)
        self.cursor.execute(insert_sql)
        self.conn.commit()


# 360daily插入数据
class Safe_daily_sqlPipeline(object):
    # 采用同步的机制写入mysql
    def __init__(self):
        self.conn = pymysql.connect(MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DBNAME, charset="utf8",
                                    use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        insert_daily_sql = """INSERT INTO ANDROID_SAFE_APP_DAILY(stat_dt,app_keys,downs,dt_type)
                                                VALUES  ("%s","%d","%d","%s")""" % (
            item["stat_dt"], int(item["app_keys"]), int(item["downs"]), item["dt_type"])
        # print(insert_daily_sql)
        self.cursor.execute(insert_daily_sql)
        self.conn.commit()


# 360手机端pipeline
class SqlserverPipelineweek(object):
    # 采用同步的机制写入mysql
    def __init__(self):
        self.conn = pymysql.connect(MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DBNAME, charset="utf8",
                                    use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        insert_top_sql = """INSERT INTO ANDROID_SAFE_APP_TOP(stat_dt,
                   app_keys,downs,dt_type,app_name,cate,sort,source,top_num,sub,category_lv3)
                VALUES  ("%s","%s","%d","%s","%s","%s","%s","%s","%d","%s","%s")""" % (
            item["stat_dt"], item["app_keys"], item["downs"], item["dt_type"], item['app_name'], item["cate"],
            item['sort'], item['source'], int(item['top_num']), item['sub'], item['category_lv3'])

        # insert_top_sql = """INSERT INTO ANDROID_SAFE_APP_TOP_TEST3(stat_dt,
        #                    app_keys,downs,dt_type,app_name,cate,sort,source,top_num,sub,category_lv3,page_num)
        #                 VALUES  ("%s","%s","%d","%s","%s","%s","%s","%s","%d","%s","%s","%s")""" % (
        #     item["stat_dt"], item["app_keys"], item["downs"], item["dt_type"], item['app_name'], item["cate"],
        #     item['sort'], item['source'], int(item['top_num']), item['sub'], item['category_lv3'], item['page_num'])

        # 插入list表中,防止app_key不变但是名字变了
        insert_list_sql = """INSERT INTO ANDROID_SAFE_APP_LIST(app_name,app_keys,app_pkg,app_md5,version_id,in_dt)
                        VALUES  ("%s","%d","%s","%s","%s","%s")""" % (
            item["app_name"], int(item["app_keys"]), item["pkgname"], item["app_md5"], item['versionname'],
            item["in_dt"])
        # 这张表是记录所有app信息,是同一个app_key只能有一个
        insert_app_sql = """INSERT  IGNORE ANDROID_SAFE_APP(app_name,app_keys,app_pkg,app_md5,version_id,in_dt,category_lv1,category_lv2)
                                VALUES  ("%s","%d","%s","%s","%s","%s","%s","%s")""" % (
            item["app_name"], int(item["app_keys"]), item["pkgname"], item["app_md5"], item['versionname'],
            item["in_dt"], item["cate"], item["sort"])
        # 存入daily这张表中,这张表同一天同一个app_key只能存一条数据
        insert_daily_sql = """INSERT IGNORE ANDROID_SAFE_APP_DAILY(stat_dt,app_keys,downs,dt_type)
                                        VALUES  ("%s","%d","%d","%s")""" % (
            item["stat_dt"], int(item["app_keys"]), int(item["downs"]), item["dt_type"])
        # print(insert_top_sql)
        # print(insert_list_sql)
        # print(insert_app_sql)
        # print(insert_daily_sql)
        self.cursor.execute(insert_top_sql)
        self.cursor.execute(insert_list_sql)
        self.cursor.execute(insert_app_sql)
        self.cursor.execute(insert_daily_sql)
        self.conn.commit()


# 腾讯应用宝pipeline
class tencentPipelineweek(object):
    # 采用同步的机制写入mysql
    def __init__(self):
        self.conn = pymysql.connect(MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DBNAME, charset="utf8",
                                    use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        insert_sql = """INSERT INTO ANDROID_QQ_APP_TOP(stat_dt,
                   app_keys,downs,dt_type,cate,sort,source,top_num,sub,app_name)
                VALUES  ("%s","%s","%d","%s","%s","%s","%s","%d","%s","%s")""" % (
            item["stat_dt"], item["app_keys"], item["downs"], item["dt_type"], item["cate"],
            item['sort'], item['source'], int(item['top_num']), item['sub'], item['app_name'])
        # 插入list表中,防止app_key不变但是名字变了
        insert_list_sql = """INSERT INTO ANDROID_QQ_APP_LIST(app_name,app_keys,app_pkg,app_md5,version_id,in_dt)
                        VALUES  ("%s","%d","%s","%s","%s","%s")""" % (
            item["app_name"], int(item["app_keys"]), item["pkgname"], item["app_md5"], item['versionname'],
            item["in_dt"])
        # 这张表是记录所有app信息,是同一个app_key只能有一个
        insert_app_sql = """INSERT  IGNORE ANDROID_QQ_APP(app_name,app_keys,app_pkg,app_md5,version_id,in_dt,category_lv1,category_lv2)
                                VALUES  ("%s","%d","%s","%s","%s","%s","%s","%s")""" % (
            item["app_name"], int(item["app_keys"]), item["pkgname"], item["app_md5"], item['versionname'],
            item["in_dt"], item["cate"], item["sort"])
        # 存入daily这张表中,这张表同一天同一个app_key只能存一条数据
        insert_daily_sql = """INSERT IGNORE ANDROID_QQ_APP_DAILY(stat_dt,app_keys,downs,dt_type)
                                        VALUES  ("%s","%d","%d","%s")""" % (
            item["stat_dt"], int(item["app_keys"]), int(item["downs"]), item["dt_type"])
        # print(insert_sql)
        # print(insert_list_sql)
        # print(insert_app_sql)
        # print(insert_daily_sql)
        self.cursor.execute(insert_sql)
        self.cursor.execute(insert_list_sql)
        self.cursor.execute(insert_app_sql)
        self.cursor.execute(insert_daily_sql)
        self.conn.commit()


# 腾讯daily插入数据
class tencent_daily_sqlPipeline(object):
    # 采用同步的机制写入mysql
    def __init__(self):
        self.conn = pymysql.connect(MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DBNAME, charset="utf8",
                                    use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        insert_daily_sql = """INSERT INTO ANDROID_QQ_APP_DAILY(stat_dt,app_keys,downs,dt_type)
                                                VALUES  ("%s","%d","%d","%s")""" % (
            item["stat_dt"], int(item["app_keys"]), int(item["downs"]), item["dt_type"])
        # print(insert_daily_sql)
        self.cursor.execute(insert_daily_sql)
        self.conn.commit()


class TencentMysqlPipeline(object):
    # 采用同步的机制写入mysql
    def __init__(self):
        self.conn = pymysql.connect(MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DBNAME, charset="utf8",
                                    use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        insert_sql = """INSERT INTO tencent_downloads(app_names,
                   software, downloads_nums, types,crawl_time,id)
                VALUES  ("%s","%d","%d","%s","%s","%d")""" % (
            item["name"], item["software"], item["downloads_nums"], item["types"], item["crawl_time"], item["id"])
        # print(insert_sql)
        self.cursor.execute(insert_sql)
        self.conn.commit()


class Tencent_from_MysqlPipeline(object):
    # 采用同步的机制写入mysql
    def __init__(self):
        self.conn = pymysql.connect(MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DBNAME, charset="utf8",
                                    use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        insert_sql = """INSERT INTO tencent_downloads2(app_names,
                   software, downloads_nums, types,crawl_time,id,pkgname,versionname)
                VALUES  ("%s","%d","%d","%s","%s","%d","%s","%s")""" % (
            item["name"], item["software"], item["downloads_nums"], item["types"], item["crawl_time"], item["id"],
            item["pkgname"], item["versionname"])
        # print(insert_sql)
        self.cursor.execute(insert_sql)
        self.conn.commit()


from twisted.enterprise import adbapi
import pymysql
import pymysql.cursors


class MysqlTwistedPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbpool = adbapi.ConnectionPool("pymysql", MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DBNAME, charset="utf8",
                                       cursorclass=pymysql.cursors.DictCursor,
                                       use_unicode=True)
        return cls(dbpool)

    def process_item(self, item, spider):
        # 使用twisted将mysql插入变成异步执行
        self.dbpool.runInteraction(self.do_insert, item)

    def do_insert(self, cursor, item):
        # 执行具体的插入
        # 根据不同的item 构建不同的sql语句并插入到mysql中
        insert_daily_sql = """INSERT INTO ANDROID_SAFE_APP_DAILY(stat_dt,app_keys,downs,dt_type)
                                                VALUES  ("%s","%d","%d","%s")""" % (
            item["stat_dt"], int(item["app_keys"]), int(item["downs"]), item["dt_type"])
        cursor.execute(insert_daily_sql)
        # insert_sql, params = item.get_insert_sql()
        # cursor.execute(insert_sql, params)
