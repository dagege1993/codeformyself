import random


def choseSeat(chose, i, N):
    result = i
    if i in chose:
        t = random.randint(1, N)
        while True:
            if t not in chose:
                break
            t = random.randint(1, N)
        chose.add(t)
        result = t
    else:
        chose.add(i)
    return result


def tick(N):
    tickNm = range(1, N + 1)
    first = random.randint(1, N - 1)
    tickDict = {1: first}
    chose = set([first])
    for i in tickNm[1:]:
        result = choseSeat(chose, i, N)
        tickDict[i] = result
    return tickDict


right = 0
N = 100
n = 100000
for i in range(n + 1):
    tickDict = tick(N)
    if tickDict[N] == N:
        right += 1
print("采集总次数:{}".format(n))
print("最后一个乘客坐在自己位置的次数:{}".format(right))
print("最后一个乘客坐在自己位置的频率:{}".format(right / n))
