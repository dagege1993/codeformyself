import requests


def getcomments(shopid):
	url = "https://www.meituan.com/meishi/api/poi/getMerchantComment"
	
	querystring = {"uuid": "6b18660b-6a64-4c45-b175-893670abbc18",
	               "platform": "1",
	               "partner": "126",
	               "originUrl": "https%3A%2F%2Fwww.meituan.com%2Fmeishi%2F91190467%2F",
	               "riskLevel": "1",
	               "optimusCode": "1",
	               "id": shopid,
	               "userId": "",
	               "offset": "0",
	               "pageSize": "10",
	               "sortType": "1"
	               }
	
	headers = {
		'Accept': "application/json",
		'Accept-Encoding': "gzip, deflate, br",
		'Accept-Language': "zh-CN,zh;q=0.9,en;q=0.8",
		'Connection': "keep-alive",
		'Host': "bj.meituan.com",
		'Referer': "https://bj.meituan.com/meishi/2412338/",
		'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36",
		'Cache-Control': "no-cache",
	}
	
	response = requests.request("GET", url, headers=headers, params=querystring)
	
	# print(response.text)
	return response
