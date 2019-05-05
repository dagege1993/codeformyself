def get_course_count(day):
    """
    :param day:日期
    :return: 全部课程数
    """
    sql = """select count(*) from COURSE WHERE  times = '%s';""" % (day)
    # 执行sql语句
    cursor.execute(sql)
    # 提交到数据库执行
    db.commit()
    # 使用 fetchone() 方法获取一条数据
    data = cursor.fetchone()[0]

    return data


def get_free_course_count(day):
    """
    :param day: 日期
    :return: 免费课程数
    """

    sql = """select count(*) from COURSE WHERE  diamondPrice ='0' AND   times = '%s';""" % (day)
    # 执行sql语句
    cursor.execute(sql)
    # 提交到数据库执行
    db.commit()
    # 使用 fetchone() 方法获取一条数据
    data = cursor.fetchone()[0]
    return data


def get_virtual_money_course_count(day):
    """
    :param day: 日期
    :return: 虚拟货币课程数
    """
    sql = """select count(*) from COURSE WHERE  diamondPrice !=0 and ID !='3-cccccccccccccccccccccc' AND times = '%s';""" % (
        day)
    # 执行sql语句
    cursor.execute(sql)
    # 提交到数据库执行
    db.commit()
    # 使用 fetchone() 方法获取一条数据
    data = cursor.fetchone()[0]
    return data


def get_renminbi_course_count(day):
    """
    :param day: 日期
    :return: 人民币课程数
    """
    sql = """select count(*) from COURSE WHERE   ID ='3-cccccccccccccccccccccc' AND times = '%s';""" % (
        day)
    # 执行sql语句
    cursor.execute(sql)
    # 提交到数据库执行
    db.commit()
    # 使用 fetchone() 方法获取一条数据
    data = cursor.fetchone()[0]
    return data


def get_applicants_all_course(day):
    """
    :param day:
    :return: 全部课程报名人次数
    """
    sql = """select sum(studyUsersCount) from COURSE WHERE times = '%s';""" % (day)
    # 执行sql语句
    cursor.execute(sql)
    # 提交到数据库执行
    db.commit()
    # 使用 fetchone() 方法获取一条数据
    data = cursor.fetchone()[0]
    return data


def get_applicants_free_course(day):
    """
    :param day:
    :return: 免费课程报名人次数
    """
    sql = """select sum(studyUsersCount) from COURSE WHERE diamondPrice =0 and times = '%s';""" % (day)
    # 执行sql语句
    cursor.execute(sql)
    # 提交到数据库执行
    db.commit()
    # 使用 fetchone() 方法获取一条数据
    data = cursor.fetchone()[0]
    return data


def get_applicants_virtual_money_course(day):
    """
    :param day:
    :return: 虚拟货币课程报名人次数
    """
    sql = """select sum(studyUsersCount) from COURSE WHERE diamondPrice !=0 and ID !='3-cccccccccccccccccccccc' and times = '%s';""" % (
        day)
    # 执行sql语句
    cursor.execute(sql)
    # 提交到数据库执行
    db.commit()
    # 使用 fetchone() 方法获取一条数据
    data = cursor.fetchone()[0]
    return data


def get_applicants_renminbi_course(day):
    """
    :param day:
    :return: 人民币课程报名人次数
    """
    sql = """select sum(studyUsersCount) from COURSE WHERE  ID ='3-cccccccccccccccccccccc' and times = '%s';""" % (day)
    # 执行sql语句
    cursor.execute(sql)
    # 提交到数据库执行
    db.commit()
    # 使用 fetchone() 方法获取一条数据
    data = cursor.fetchone()[0]
    return data


if __name__ == '__main__':
    import pymysql
    db = pymysql.connect("192.168.103.31", "root", "adminadmin", "fluent")
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    day = '2019-03-11'
    course_count = get_course_count(day)
    print('全部课程数', course_count)

    free_course_count = get_free_course_count(day)
    print('免费课程数', free_course_count)

    virtual_money_course_count = get_virtual_money_course_count(day)
    print('虚拟货币课程数', virtual_money_course_count)

    renminbi_course_course_count = get_renminbi_course_count(day)
    print('人民币课程数', renminbi_course_course_count)
    print('-----------------------------------------')
    applicants_all_course = get_applicants_all_course(day)
    print('全部课程报名人次数', applicants_all_course)

    applicants_free_course = get_applicants_free_course(day)
    print('免费课程报名人次数', applicants_free_course)

    applicants_virtual_money_course = get_applicants_virtual_money_course(day)
    print('虚拟货币课程报名人次数', applicants_virtual_money_course)

    applicants_renminbi_course = get_applicants_renminbi_course(day)
    print('虚拟货币课程报名人次数', applicants_renminbi_course)
    print('-----------------------------------------')

    # 做简单数据验算
    if int(applicants_all_course) != int(applicants_renminbi_course) + int(applicants_virtual_money_course) + int(
            applicants_free_course):
        print('求和后数据不等')
    if int(course_count) != int(free_course_count) + int(virtual_money_course_count) + int(
            renminbi_course_course_count):
        print('求和后数据不等')
