import random
import time

random.randint(1, 2)
line = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '   ' + "http://www.taobao.cim/" + str(random.randint(1, 20))
print(line)
# with open("page_views.dat", r)as f:
#     line
