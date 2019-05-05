import copy
import csv
import datetime
import re
import time

import pymysql

result_list = []


def reader_csv():
    csv_reader = csv.reader(open("safe0218.csv", ))
    for i, row in enumerate(csv_reader):
        # print(row)
        if i > 0:
            row[1:] = get_times(row)
            result_list.append(row)
        else:
            head_list = copy.deepcopy(row)
    # print(result_list)

    # 输出结果
    filename = 'result0218' + '.csv'
    with open(filename, 'a+', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(head_list)
        for row in result_list:
            writer.writerow(row)


# 获取时间对应的那个参数
def get_times(row):
    insuranceTitle = row[0]
    research_result = []
    for times in row[1:]:
        # print(times)
        years = re.findall('(.*)年', times)[0]
        months = re.findall('/(.*)月', times)[0]
        number = re.findall('第(.*)次公示', times)[0]
        # print(years, months, number)
        db = pymysql.connect("192.168.103.31", "root", "adminadmin", "water_safe")
        cursor = db.cursor()
        sql = """select joinPerson from PLANS2 where insuranceTitle='%s' and years='%s' and months='%s' and schedule='%s';""" % (
            insuranceTitle, years, months, number)
        print(sql)
        cursor.execute(sql)
        db.commit()
        # 有一条记录
        results = cursor.fetchone()
        if results:
            result = str(results[0])
        else:
            result = '0'
        research_result.append(result)
    db.close()
    return research_result


def adjust_result():
    import pandas as pd
    data = pd.read_excel('result0218.xlsx')
    # data = pd.read_csv('result0218.csv')  # 读取这个文件就报错,只能改为xlsx就可以,编码格式也改了还是不行
    columns = data.columns
    for i, column in enumerate(columns):
        if i > 0:
            column_value = data[column]  # 获取某一列的值
            print(column_value)
            sum_result = column_value.sum()  # 某一列求和,
            if sum_result == 0:
                print(column)
                data.drop([column], axis=1, inplace=True)  # 把这一列累加为0 的列删除

    # 输出结果
    data.to_csv('2_adjust_result0218_2.csv')


def get_lost_again(row):
    new_row = []
    for i in row:
        if i != '0':
            flag = i
            break  # 这一个循环是为了找到第一个不为零的值
    for j in row:
        if j == '0':
            j = flag
        else:
            flag = j
        new_row.append(j)
    print(new_row)
    return new_row


def adjust_result_again():
    """
    为了把空值补上
    :return: 当前这个计划这次公示可能为空,就取下一次的值直到不为零为止
    """
    result_list = []
    # csv_reader = csv.reader(open("adjust_result.csv", ))
    # csv_reader = csv.reader(open("adjust_result0218.csv", encoding='utf-8'))
    csv_reader = csv.reader(open("2_adjust_result0218_2.csv"))
    # csv_reader = csv.reader(open("adjust_result0218.csv", encoding='ISO-8859-1'))
    for i, row in enumerate(csv_reader):
        print(row)
        if i > 0:
            change_row = row[2:]
            row[1:] = get_lost_again(change_row)  # 处理缺失的值
            result_list.append(row)

    # 输出结果
    filename = '3_fill_null_result0218' + '.csv'
    with open(filename, 'a+', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        for row in result_list:
            writer.writerow(row)


if __name__ == '__main__':
    # 去读文件然后根据时间和类别进行查找,生成的文件result0218.csv
    # reader_csv()
    # 把一列的空值全部删除,生成文件adjust_result0218.csv
    # adjust_result()
    # 把当月的空值用上一个月的值替代,这里需要先把编码格式换一下,虽然写入文件的时候已经指定了编码格式,不过没什么用看来
    adjust_result_again() #这里生成的fill_null_result0218.csv文件需要复制一下names和时间,从adjust_result0218.csv复制
