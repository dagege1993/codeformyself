# 从redis 获取一个随机的token,这个token是设置了7天的过期时间
import random

import redis


def get_token():
    conn = redis.StrictRedis(host='localhost')
    token_len = conn.llen('token')
    result = conn.lindex("token", random.randint(0, token_len - 1))
    result = str(result, encoding="utf8")
    return result
