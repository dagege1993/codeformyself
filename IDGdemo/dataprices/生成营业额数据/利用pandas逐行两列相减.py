import pandas as pd

data = pd.read_excel(
    r'C:\Users\Administrator.DESKTOP-DV7S27B\Desktop\IDGdemo\dataprices\生成营业额数据\studyUsersCount - 副本.xlsx',
    sheet_name='Sheet1')
research_times = ["2018-11-16", "2018-11-17", "2018-11-21", "2018-11-22", "2018-11-23",
                  "2018-11-26", "2018-11-27", "2018-11-28", "2018-11-29", "2018-11-30",
                  "2018-12-03", "2018-12-04", "2018-12-05", "2018-12-06", "2018-12-07", ]

for i, days in enumerate(research_times):
    if days == research_times[-1]:
        break
    else:
        starts = data[days]
        end = data[research_times[i + 1]]
        data[days] = end - starts
        print(data[days])

        # 得把最后一列数据给去掉
        del data[research_times[-1]]
data.to_excel(r'C:\Users\Administrator.DESKTOP-DV7S27B\Desktop\IDGdemo\dataprices\生成营业额数据\输出.xlsx', header=None)
