#!coding:utf-8

import time
import redis

if __name__ == "__main__":
    try:
        conn = redis.StrictRedis(host='localhost')
        conn.set('name', '蒋乐哥哥')
        conn.expire('name', 10)  # 设置键的过期时间为10s

        for item in range(12):
            value = conn.get('name')
            if value != None:
                print(value.decode('utf8'))
            else:
                print('the key has been deleted...')
                break
            time.sleep(1)
    except Exception as err:
        print(err)
