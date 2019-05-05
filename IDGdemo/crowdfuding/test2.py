# encoding=utf8
tt = {
    "code": 0,
    "msg": "",
    "data": {
        "pageNo": 0,
        "noticeGroupHistoryList": [
            {
                "year": "2016年",
                "noticeGroupHistoryDetailVOList": [
                    {
                        "groupNo": "3d654175a2e74cdc8bdb464de5c825dc",
                        "title": "12月第2期",
                        "totalAmount": "110000.00",
                        "totalMember": 2
                    },
                    {
                        "groupNo": "4c247983644d43868b34d8c712d847fe",
                        "title": "12月第1期",
                        "totalAmount": "30000.00",
                        "totalMember": 1
                    },
                    {
                        "groupNo": "a0adfc7bc1b543639311ac7af26ee5d1",
                        "title": "11月第1期",
                        "totalAmount": "20000.00",
                        "totalMember": 1
                    }
                ]
            },
            {
                "year": "2017年",
                "noticeGroupHistoryDetailVOList": [
                    {
                        "groupNo": "4a46369e035698278444ee",
                        "title": "5月 第2期",
                        "totalAmount": "1410000.00",
                        "totalMember": 10
                    },
                    {
                        "groupNo": "68464b9a833576a51e0951",
                        "title": "5月 第1期",
                        "totalAmount": "2020019.10",
                        "totalMember": 17
                    },
                    {
                        "groupNo": "4b4dd0a61722b520ffaeee",
                        "title": "4月 第2期",
                        "totalAmount": "760010.80",
                        "totalMember": 8
                    }
                ]
            }
        ]
    }
}
detail_list = []
data = tt.get('data')
group_history = data.get('noticeGroupHistoryList')
for times in group_history:  # 因为group_history是个列表
    year = times.get('year')
    for group in times.get('noticeGroupHistoryDetailVOList'):
        group['year'] = year
        detail_list.append(group)
# print(detail_list)

# ll = '6月2期划款公示'
ll = '3月 第2期划款公示'
import re

result = re.findall('(\d+)月', ll)
print(result)

result2 = re.findall('(\d)期', ll)
print(result2)