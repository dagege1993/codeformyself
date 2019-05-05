import math
from datetime import datetime

tt = (2146,)
for i in tt:
    # print(i)
    pass
# print(''.join(tt))
# print(map(str, tt))
total = 2167
id_count = 2146
if total > id_count:
    # print(111)
    pass

if total > id_count:
    total_int = int(total)
    total_page = math.ceil(total_int / 20)  # 向上取整
    total_page += 1
    for page in range(1, int(total_page)):
        # print(page)
        pass
from datetime import datetime
today = datetime.now()
log_file_path = "log/{}-{}-{}.log".format(today.year, today.month, today.day)
print(log_file_path)
