import time
import redis

if __name__ == "__main__":
    try:
        conn = redis.StrictRedis(host='192.168.103.31')
        token_list = [
            "014ec4b02082013791000a5864608e66",
        ]
        for token in token_list:
            conn.lpush("token", token)
        conn.expire('token', 14 * 24 * 60 * 60)  # 设置键的过期时间为14day
    except Exception as err:
        print(err)
