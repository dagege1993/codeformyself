# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from scrapy.conf import settings
from fast_fluent.settings import *


class FastFluentPipeline(object):
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
        agentinfo['_id'] = agentinfo.pop("id")
        self.port.insert(agentinfo)
        return item


import pymysql


class MysqlPipeline(object):
    # 采用同步的机制写入mysql
    def __init__(self):
        self.conn = pymysql.connect(MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DBNAME, charset="utf8",
                                    use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        # insert_sql = """INSERT INTO COURSE(ID,
        #             diamondPrice, studyUsersCount, translatedTitle,times)
        #           VALUES  ("%s","%d","%d","%s","%s")""" % ('5ade9c3d636f6e67610000af', 0, 0, '测试', '2018-11-15')
        insert_sql = """INSERT INTO COURSE(ID,
                   diamondPrice, studyUsersCount, translatedTitle,times)
                VALUES  ("%s","%d","%d","%s","%s")""" % (
            item["ID"], item["diamondPrice"], item["studyUsersCount"], item["translatedTitle"], item["times"])

        self.cursor.execute(insert_sql)
        self.conn.commit()


class Mysql_Course_ID_Pipeline(object):
    def __init__(self):
        self.conn = pymysql.connect(MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DBNAME, charset="utf8",
                                    use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        insert_sql = """INSERT ignore COURSE_ID(ID,insert_time) VALUES  ("%s","%s")""" % (
        item["ID"], item["insert_time"])

        self.cursor.execute(insert_sql)
        self.conn.commit()
