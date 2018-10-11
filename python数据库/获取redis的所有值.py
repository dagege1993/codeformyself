import redis

# REDIS_HOST = '127.0.0.1'
REDIS_HOST = '192.168.107.38'

# Redis端口
REDIS_PORT = 6379

# Redis密码，如无填None
REDIS_PASSWORD = None

MAX_SCORE = 100
MIN_SCORE = 0


class RedisClient(object):
	def __init__(self):
		self.db = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, decode_responses=True)
	
	def all_proxy(self, redis_key):
		"""
		获取全部代理
		:return: 全部代理列表
		"""
		return self.db.zrangebyscore(redis_key, MIN_SCORE, MAX_SCORE)


print(RedisClient().all_proxy('sina'))
print('*********************************************************************')
print(RedisClient().all_proxy('General_pool'))
print('*********************************************************************')
# print(RedisClient().all_proxy('333'))
