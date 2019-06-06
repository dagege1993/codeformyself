# coding:utf8

import time
from tasks import alicdn

# for x in range(2, 3):
#     print(x)
#     time.sleep(x)
#     print(alicdn.audit_cdn_logs.apply_async(args=(x,)))
# print(alicdn.query_top_url('img4.weegotr.com'))
print(alicdn.audit_cdn_logs.apply_async(args=(3,)))
