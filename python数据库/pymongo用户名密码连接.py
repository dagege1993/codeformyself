import json
import re

from pymongo import MongoClient
from dotenv import find_dotenv, load_dotenv

# # seeker是创建的数据库账号
client = MongoClient(host='192.168.111.39', port=27017)
db_auth = client.admin
db_auth.authenticate("jkspider", "adminadmin")
db = client['jkspider']['duolabao']

queryArgs = {'entName': '洛阳市站区新大华超市'}
search_res = db.find(queryArgs).sort('entName', -1)

print(search_res)
import csv

csvFile2 = open('lipeipei.csv', 'a', newline='', encoding='utf-8')  # 设置newline，否则两行之间会空一行
writer = csv.writer(csvFile2)
data_list = []
for record in search_res:
	# data_list.append(record)
	# print(data_list)
	with open('test.txt', 'a') as f:
		f.write(record)

# csvFile3 = open('lipeipei.csv', 'a', newline='', encoding='utf-8')
# 	writer2 = csv.writer(csvFile3)
# 	for key in record:
# 		writer2.writerow([key, record[key]])
# csvFile3.close()

# m = len(data_list)
# for i in range(m):
# 	writer.writerow(data_list[i].values())
# csvFile2.close()

# # 从列表写入csv文件
# csvFile2 = open('csvFile2.csv', 'w', newline='')  # 设置newline，否则两行之间会空一行
# writer = csv.writer(csvFile2)
# m = len(data)
# for i in range(m):
# 	  writer.writerow(data[i])
# csvFile2.close()
# # 从字典写入csv文件
# dic = {'张三': 123, '李四': 456, '王二娃': 789}
# csvFile3 = open('csvFile3.csv', 'w', newline='')
# writer2 = csv.writer(csvFile3)
# for key in dic:
# 	  writer2.writerow([key, dic[key]])
# csvFile3.close()

# 从字典写入csv文件
# dic = {'张三':123, '李四':456, '王二娃':789}
# csvFile3 = open('lipeipei.csv','w', newline='')
# writer2 = csv.writer(csvFile3)
# for key in dic:
#   writer2.writerow([key, dic[key]])
# csvFile3.close()


# 链接虚拟试试
# client = MongoClient(host='192.168.160.131', port=27017)
# client = MongoClient(host='192.168.107.37', port=27017)
# db_auth = client.admin
# db_auth.authenticate("jinke", "jinke")
# print(db_auth.authenticate("test", "test"))
# db = client['hlz']['test']

# result = {"company": "深圳万国食尚餐饮管理有限公司333",
#           "company_year": "2016年04月22日333",
#           "company_type": "有限责任公司（法人独资）333",
#           "company_address": "珠市口东大街333",
#           "company_license_number": "333"
#
#           }
# for i in range(10):
# db = client['hlz']['test']
# db.insert(result)
# ll = db.find()
# print(ll)

# response = re.findall('{.*}', result)
# # print(2, response)
#
# client = MongoClient(host='192.168.107.37', port=27017)
# db = client['hlz']['IDcard']
# for i in response:
# 	# print(1, i)
# 	# print(json.loads(i))
# 	db.insert(json.loads(i))


# import requests
# import urllib3
#
# urllib3.disable_warnings()
# url = "https://authgtj.alipay.com/login/index.htm"
#
# payload = "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"support\"\r\n\r\n000001\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"CtrlVersion\t\"\r\n\r\n1,1,0,1\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"loginScene\t\"\r\n\r\nindex\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"rds_form_token\t\"\r\n\r\nV6AmUw45MJAkEDYnoTHmYGxTn751OAJz\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"logonId\t\"\r\n\r\n18273711329\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"superSwitch\t\"\r\n\r\ntrue\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"noActiveX\t\"\r\n\r\nfalse\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"passwordSecurityId\t\"\r\n\r\nweb|authcenter_querypwd_login|c6e5d2a2-bc26-4f67-8c17-57b01b565c97RZ12\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"qrCodeSecurityId\t\"\r\n\r\nweb|authcenter_qrcode_login|f5d1ebd1-3c91-4f8e-857d-424c4e20e867RZ12\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"J_aliedit_using\t\"\r\n\r\ntrue\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"password\t\"\r\n\r\nF4/aTLH6ntGha+C3msZWFH0XmPFbJkHOMLjsJzFHY+LM7EeLhX9U8JbZbsSOOH+5lOs/SSNkNsE4jWg+dHO+MYebxyfw6hF9tJnMLeTAK5bsrHCgw5PaQzvN6hYQJfimIOix8VGjwUwUgxwuOScTwA+KY8J6zxs8G6GXDJx070j9yIiUccHRlCq6NouZRBlgqsgIpvhe3pVTEttoFVPGcsL0+89W/HJCp6sp5Yxf43YT9tJkXonTxXzFCoMtHBp1R8VukGAifKoDtxp0lCo24+lUJ067tVODUo544iLhTf7j2JG3qs/M4HRC3aoiLAcOGrn20V+Wqwjcm4qYXOAahw==\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"J_aliedit_key_hidn\t\"\r\n\r\npassword\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"J_aliedit_uid_hidn\"\r\n\r\nalieditUid\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"REMOTE_PCID_NAME\t\"\r\n\r\n_seaside_gogo_pcid\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"alieditUid\"\r\n\r\nb929f777ed3e17c202e5e8e5de057b30\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"security_activeX_enabled\t\"\r\n\r\nfalse\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"preCheckTimes\t\"\r\n\r\n5\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"ua\t\"\r\n\r\n043YlF/THtKfkR3THpBd0FyQxw=|YVF/JgZHLV0wXzgYNhYiGTkXN2IJZQNuG2pKFUo=|YFF/JhUjFzkOOxUmFiIWOAw7AS8cJxclCzgKMAIsHyQUJgg7CT8NUg0=|Z1RnSRAwWixaKFlhTGECdQNpRSZII1EySWUEaQYrRShNJkpnDGAGYRs3XStEZEpqAHYAcgM7FjtOO05iAmEKbBs3VjtUeRd8EHlEM0MtElcfaSxxK0p+N11sPVUIbFgiWWoaLx8vGFAdfCofXmkFb1l2JEMCawUwRgg5SjFhL0QDdyZ7Pl9kLXYEbxRGdSAEcRcoDGsYcxUqS34aLR17Gi8dLx0rT3lNd0V3RXdFd0VyRSUefU98TH1dAl0=|ZlVlS2s/C0gncAUzBEsDQCluKHMfciRuAVofZTNfal1uI2AoUHAv|ZV9xUTJFM1k4XzNFIlIPYQxpAm4zAzECOAo7CDMANQI0AjlkVGBTZ119Ig==|ZF9xCChJOUwvQWFZIAB0F3lZYUEiTCdVNk1tQ2MRfxxqDmMTfFxkRBF6FicXNxk5TyJVNF5+RiJBL145RmhIOVI9SiFNKURkXCUFcBt3V29ebF9xUTdaOxsjEjwcfQx9XWVWbEJiAnIfaht8DCwUTW0iTzdcMlw/HzERXTpMPVw/TSoKJAQzHy0PJXAbdxF8CXhaFkBiUWNPfURmM1g0ADYPLVdjVX5cH20fcRZDJEQNZhA9CjsOIhMnBS9mLHo1e1V3GXIbfF4bfB10GTIQUTtLJkkuAzcMIBI+DzkCNxshEjBhAmYFdR4zBDUALB0pCScHJwl/D3gfMUc3QCcJKXwXe0p6WnRUdFp6NVggSyVLKAUyHiwOJHEadhB9CHlbF0FjUGJOfEVnMlk1ATcOLFZiVH9dHmwecBdCJUUMZxE8CzoPIxImBC5nLXs0elR2GHMafV8afRx1GDMRUDpKJ0gvAjYNIRM/DjgDNhogEzFgA2cEdB8yBTQBLRwoCCYGJggoSyVOPF8kCGkEa0tlRWVLa0tlRWVLa0tlVm1db0FyQHpIZlZgTn1GdkRqWWtdb0FzXW8wT2FBMVI+WDVaekJzSXhNdlh4GW8CawxgQHhYaCtxG3Aecx5ENUMmbAhdDCxTDA==|a11zKgoqBD4OPhAkFTsONQY0azQ=|al1zKgoqBF1mUWRKeU13KAY0GjoaNAc1AzUDXAM=|aV5wKQl7GGkYbQBwFks7SilCLlwrXX1TCjAEPxEhGit0WmhGZkZoW2hYaFsEWw==|aF1zKgp4G2obbgNzFUg4SSpBLV8oXn5QY01+TX1JeiV6|b1t1LAx+HWwdaAV1E04+TyxHK1kuWHhWYFB+TGJRYVNoXgFe|blp0LQ1/HG0caQR0Ek8/Ti1GKlgvWXlXYVF/TWNQYFBkVwhX|bVl3Lg58H24fagd3EUw8TS5FKVssWnpUYlJ8TmBTY1RjUA9Q|bFh2Lw99Hm8eawZ2EE09TC9EKFotW3tVY1N9T2FSY1FgWgVa|c0VrMhJadRt2E3gUO1stQWFPdUF6VGVTZ0l6TnpKeiV6|ckVrMhJadRt2E3gUO1stQWFPFiwZKwU0AzZpR3Vbe1t1RnJJe0sUSw==|cURqMxNhAnMCdxpqDFEhUDNYNEYxR2dJe1VmUmlebjFu|cEVrMhJadRt2E3gUO1stQWFPfFJhVGZUZzhn|d0JsNRVdchxxFH8TPFwqRmZIelRnUmNVZjlm|dkVrWnRBb1xvVXtIfkxiVW5AdUJsV3lKf1FiVnhJclxsW3VFc11tXHJCclxvQXpUZVV7SnlXZlQL\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW--"
# headers = {
# 	'content-type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
# 	'Host': "authgtj.alipay.com",
# 	'Connection': "keep-alive",
# 	'Content-Length': "3113",
# 	'Cache-Control': "no-cache",
# 	'Origin': "https://auth.alipay.com",
# 	'Upgrade-Insecure-Requests': "1",
# 	'Content-Type': "application/x-www-form-urlencoded",
# 	'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36",
# 	'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
# 	'Referer': "https://auth.alipay.com/login/index.htm",
# 	'Accept-Encoding': "gzip, deflate, br",
# 	'Accept-Language': "zh-CN,zh;q=0.9,en;q=0.8",
# 	'Cookie': "JSESSIONID=RZ12PYEXKgU5qdAEPIfYZZH9q0kvaDauthRZ12; mobileSendTime=-1; credibleMobileSendTime=-1; ctuMobileSendTime=-1; riskMobileBankSendTime=-1; riskMobileAccoutSendTime=-1; riskMobileCreditSendTime=-1; riskCredibleMobileSendTime=-1; riskOriginalAccountMobileSendTime=-1; cna=U/3KEwSmeTwCAbdRtUKnmqQ7; NEW_ALIPAY_TIP=1; unicard1.vm=\"K1iSL16SV9EvE/EboTdxcg==\"; _uab_collina=153604928557284578550913; _umdata=C234BF9D3AFA6FE7CCE5C39C37F8091298FCAAC6876B100E55D5AF6D5086FE618FE2011882956315CD43AD3E795C914CD45591856BA8D2D7118C17684E9561D9; ssl_upgrade=0; session.cookieNameId=ALIPAYJSESSIONID; LoginForm=alipay_login_auth; CLUB_ALIPAY_COM=2088702698723581; iw.userid=\"K1iSL16SV9EvE/EboTdxcg==\"; ali_apache_tracktmp=\"uid=2088702698723581\"; spanner=MsiJ5FZdTxJxigLqzLQqQmwmRy09X+pw; zone=RZ12A; ALIPAYJSESSIONID=RZ12PYEXKgU5qdAEPIfYZZH9q0kvaDauthRZ12; ctoken=2AXhilooXstgHfWS; umt=L112a7e6762798042dde51e29775a4aa6; JSESSIONID=6A74DE29E24B9CA63A61DA8F492B76AE; rtk=VQ4WkrHQtPkbExooBQbW+EUebFDJZq3seefrZzFYLg0CbsAyzD/",
# 	'Postman-Token': "97d20951-8e0b-3b80-f92d-0bdf1be199e0"
# }
#
# response = requests.request("POST", url, data=payload, headers=headers, verify=False)
#
# print(response.text)
#
