import redis

if __name__ == "__main__":
    try:
        conn = redis.StrictRedis(host='192.168.103.31')
        # token_list = ['pR_jym8DI7X-_ytajRJEegYU0G1tjvpIEj8Nf7Zkd-0=']
        token_list = ['78BL66lmZ3E-eIxaV2hAyCXgnxrijYgl_IbAw0YQSCs=']  # 2018/12/04下午两点
        for token in token_list:
            conn.lpush("AuthorizationV2", token)
            conn.expire('AuthorizationV2', 14 * 24 * 60 * 60)  # 设置键的过期时间为7day
    except Exception as err:
        print(err)
