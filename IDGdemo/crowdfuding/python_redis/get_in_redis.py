# 从redis 获取一个随机的token,这个token是设置了7天的过期时间
import random
import redis



#之前用的是列表存储,后面不知道为啥
def get_authorizationV2_in_redis():
    conn = redis.StrictRedis(host='192.168.103.31')
    token_len = conn.llen('AuthorizationV2')
    result = conn.lindex("AuthorizationV2", random.randint(0, token_len - 1))
    result = str(result, encoding="utf8")
    return result


if __name__ == '__main__':
    # print(get_authorizationV2_in_redis())
    get_authorizationV2_in_redis()
