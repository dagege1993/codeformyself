import json

import redis

msg = {
    "hotel_id": "123",
    "checkin": "345",
    "checkout": "567",
    "roomfilters": "666"
}
key = json.dumps(msg)
print(key)
r = redis.Redis(host='localhost', port=6379)

cache_result = r.get(key)
print(cache_result)

if cache_result is None:
    cache_result = {'rooms': '111', 'hotel_name': '222', 'currency': 'CNY', 'timezone': '+08:30:00'}
    r.set(key, cache_result)
    r.expire(key, 100)
