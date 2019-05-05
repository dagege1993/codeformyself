import pymysql
from twisted.enterprise import adbapi
from twisted.internet import reactor


class MysqlTwistedPipeline():
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls):
        # 需要在setting中设置数据库配置参数
        dbparms = dict(
            host='192.168.103.31',
            db='company',
            user='root',
            passwd='adminadmin',
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor,
            use_unicode=True,
        )
        # 连接ConnectionPool（使用MySQLdb连接，或者pymysql）
        dbpool = adbapi.ConnectionPool("MySQLdb", **dbparms)  # **让参数变成可变化参数
        return cls(dbpool)  # 返回实例化对象

    def process_item(self, item, spider):
        # 使用twisted将MySQL插入变成异步执行
        query = self.dbpool.runInteraction(self.do_insert, item)
        # 添加异常处理
        query.addCallback(self.handle_error)

    def handle_error(self, failure):
        # 处理异步插入时的异常
        print(failure)

    def do_insert(self, cursor, item):
        # 执行具体的插入
        insert_sql = """
                    insert into jobbole_artitle(name, base_url, date, comment)
                    VALUES (%s, %s, %s, %s)
                """
        cursor.execute(insert_sql, (item['name'], item['base_url'], item['date'], item['coment'],))


twisted = MysqlTwistedPipeline()
print(twisted)
print(dir(twisted))
