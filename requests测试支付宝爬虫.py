import re

import requests
import scrapy

# headers = {
# 	"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
# 	"Accept-Encoding": "gzip, deflate, br",
# 	"Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
# 	"Cache-Control": "max-age=0",
# 	"Connection": "keep-alive",
# 	"Cookie": 'JSESSIONID=RZ11sniFjk5ZJahwKDLnFzaTByIRcSauthRZ12GZ00; mobileSendTime=-1; credibleMobileSendTime=-1; ctuMobileSendTime=-1; riskMobileBankSendTime=-1; riskMobileAccoutSendTime=-1; riskMobileCreditSendTime=-1; riskCredibleMobileSendTime=-1; riskOriginalAccountMobileSendTime=-1; cna=U/3KEwSmeTwCAbdRtUKnmqQ7; NEW_ALIPAY_TIP=1; unicard1.vm="K1iSL16SV9EvE/EboTdxcg=="; ctoken=vqBPSGU_o9W3r2Dp; LoginForm=alipay_login_home; alipay="K1iSL16SV9EvE/EboTdxcoRDpFzeOOTxKbr+KpATyg=="; CLUB_ALIPAY_COM=2088702698723581; iw.userid="K1iSL16SV9EvE/EboTdxcg=="; ali_apache_tracktmp="uid=2088702698723581"; session.cookieNameId=ALIPAYJSESSIONID; ALIPAYJSESSIONID=RZ11sniFjk5ZJahwKDLnFzaTByIRcSauthRZ12GZ00; zone=GZ00D; JSESSIONID=94327DFBFB5AECA4472BD4EE7C289AFC; ssl_upgrade=0; spanner=7u+Ekc596bXf8rKDhs69LOypZPkuFuAq; rtk=frZXGQy1tk/7aN88mr7M0aOLe9ZoIpoZMa63yCcRnx4CZ1YJyHq',
# 	"Host": "consumeprod.alipay.com",
# 	"Referer": "https://my.alipay.com/portal/i.htm?referer=https%3A%2F%2Fauthgtj.alipay.com%2Flogin%2FhomeB.htm",
# 	"Upgrade-Insecure-Requests": '1',
# 	"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
#
# }
# response = requests.get('https://consumeprod.alipay.com/record/standard.htm', headers=headers)
# result = response.text
# print(result)


import requests

url = "https://consumeprod.alipay.com/record/standard.htm"

headers = {
	'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
	'Accept-Encoding': "gzip, deflate, br",
	'Accept-Language': "zh-CN,zh;q=0.9,en;q=0.8",
	'Cache-Control': "no-cache",
	'Connection': "keep-alive",
	'Cookie': 'JSESSIONID=RZ11sniFjk5ZJahwKDLnFzaTByIRcSauthRZ12GZ00; mobileSendTime=-1; credibleMobileSendTime=-1; ctuMobileSendTime=-1; riskMobileBankSendTime=-1; riskMobileAccoutSendTime=-1; riskMobileCreditSendTime=-1; riskCredibleMobileSendTime=-1; riskOriginalAccountMobileSendTime=-1; cna=U/3KEwSmeTwCAbdRtUKnmqQ7; NEW_ALIPAY_TIP=1; unicard1.vm="K1iSL16SV9EvE/EboTdxcg=="; session.cookieNameId=ALIPAYJSESSIONID; JSESSIONID=94327DFBFB5AECA4472BD4EE7C289AFC; ssl_upgrade=0; spanner=7u+Ekc596bXf8rKDhs69LOypZPkuFuAq; ctoken=eYRB64HfRNo3Hz6P; LoginForm=alipay_login_auth; alipay="K1iSL16SV9EvE/EboTdxcoRDpFzeOOTxKbr+KpATyg=="; CLUB_ALIPAY_COM=2088702698723581; iw.userid="K1iSL16SV9EvE/EboTdxcg=="; ali_apache_tracktmp="uid=2088702698723581"; ALIPAYJSESSIONID=RZ11dj5iw9IxolbKXyjFsWM3RBwQEAauthRZ12GZ00; zone=GZ00D; rtk=L0eXa+tjNGgBNakkb0B2rNofz5VOSPOV2NgFtVvqHEKsVj/UtnR',
	'Host': "consumeprod.alipay.com",
	'Referer': "https://my.alipay.com/portal/i.htm?referer=https%3A%2F%2Fauthgtj.alipay.com%2Flogin%2FhomeB.htm",
	'Upgrade-Insecure-Requests': "1",
	'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
	'Postman-Token': "29060b25-f3cc-aff8-a82f-4eacb862c218"
}

response = requests.request("GET", url, headers=headers)

print(response.text)
response_decode = response.text.encode('utf-8').decode('utf-8')
print(response_decode)

page_sel = scrapy.Selector(text=response.text)

monney = page_sel.xpath('//*[@id="J-item-1"]/td[4]/span/text()').extract_first()
print(monney)
