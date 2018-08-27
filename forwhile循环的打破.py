lists = [1, 2, 3, 4, 5, 6, 7, 8]
orderList = 'break'
pageNum = 1
for i in lists:
	while len(orderList) != 1000:
		pageNum += 1
		if len(orderList) == 1000:
			continue
		if orderList == 'break':
			print(pageNum)
			break

# for i in lists:
#
# 	if orderList == 'break':
# 		print('测试for循环的break')
# 		print(i)
# 		break


# 		while i < len(json_data_list):
# 			pageNum += 1
# 			if len(orderList) == 1000:
#
# 		spider_data['pageNum'] = pageNum
# 		orderList = spider(json_parameter, spider_data, url, parameter)
#
#
# while len(orderList) == 1000:
# 	pageNum += 1
# 	spider_data['pageNum'] = pageNum
# 	orderList = spider(json_parameter, spider_data, url, parameter)
# 	if orderList == 'break':
# 		j = 0
# 		break



