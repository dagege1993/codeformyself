import pandas as pd

# df = pd.read_excel(
#     '/Users/huangjack/PycharmProjects/codeformyself/flashtripdemo/处理csv文件/线上酒店城市增加名单（分级）(1).xlsx')  # 这个会直接默认读取到这个Excel的第一个表单
# country_list = df['country'].tolist()
# city_list = df['city'].tolist()
# level_list = df['评级'].tolist()
# if len(country_list) == len(city_list) == len(level_list):
#     double_list = [(city_list[i], level_list[i]) for i in range(len(city_list))]
#     # print(double_list)
#
# country_city = dict(zip(double_list, country_list))
#
# print(country_city)

df = pd.read_excel(
    '/Users/huangjack/PycharmProjects/codeformyself/flashtripdemo/处理csv文件/亚洲城市.xlsx')  # 这个会直接默认读取到这个Excel的第一个表单
country_list = df['国家'].tolist()
city_list = df['城市'].tolist()
level_list = df['评级'].tolist()
if len(country_list) == len(city_list) == len(level_list):
    double_list = [(city_list[i], level_list[i]) for i in range(len(city_list))]
    # print(double_list)

country_city = dict(zip(double_list, country_list))

print(country_city)
