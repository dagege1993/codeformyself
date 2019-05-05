import random
import redis


# city = '苏州'
# if city == '上海' or city == '郑州':
#     print('啊哈')
# 从redis 获取一个随机的token,这个token是设置了7天的过期时间
def get_token():
    conn = redis.StrictRedis(host='192.168.103.31')
    token_len = conn.llen('token')
    result = conn.lindex("token", random.randint(0, token_len - 1))
    result = str(result, encoding="utf8")
    return result


def storeId_city():
    sql = """select storeId,storeName,city,city_level from SHOP_DETAIL WHERE web_queue !='' and storeStar is not Null GROUP BY storeId """
    cursor.execute(sql)
    data_list = cursor.fetchall()
    df = pd.DataFrame(list(data_list))  # 转换成DataFrame格式
    print(df)

if __name__ == '__main__':
    print(get_token())
