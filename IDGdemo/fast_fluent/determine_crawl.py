from pymongo import MongoClient
from fast_fluent.settings import *


# 查询当前用户是否已经在数据库,返回是个数,0是不在,1是在
def get_user(user_id):
    client = MongoClient(host=MONGODB_HOST, port=MONGODB_PORT)
    db = client[MONGODB_DBNAME][MONGODB_DOCNAME]
    query_args = {'_id': user_id}
    search_res = db.find(query_args)
    return search_res.count()
