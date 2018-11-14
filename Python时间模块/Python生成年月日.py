import time

localTime = time.localtime(time.time())
strTime = time.strftime("%Y-%m-%d", localTime)
print(strTime)