import requests
import re

url = "https://www.tripadvisor.cn/Hotel_Review-g186605-d212688-Reviews-Clontarf_Castle_Hotel-Dublin_County_Dublin.html"

payload = ""
headers = {
    'User-Agent': "PostmanRuntime/7.11.0",
    'Accept': "*/*",
    'Cache-Control': "no-cache",
    # 'Postman-Token': "f3fced24-15d9-4c70-8ba6-8ea4ca36a788,92246767-a78a-4453-b5c6-b61b368e8a1e",
    'Host': "www.tripadvisor.cn",
    # 'cookie': "TASession=%1%V2ID.D8477779FA3E751F6E3DFE0F58CB9BC0*SQ.175*LP.%2FHotel_Review-g294265-d2435463-Reviews-Park_Avenue_Rochester_Hotel-Singapore%5C.html*LS.DemandLoadAjax*PD1.1*GR.12*TCPAR.81*TBR.99*EXEX.8*ABTR.59*PHTB.78*FS.4*CPU.3*HS.recommended*ES.popularity*DS.5*SAS.popularity*FPS.oldFirst*LF.zhCN*FA.1*DF.0*TRA.false*LD.294265; ServerPool=A; TATravelInfo=V2*AY.2019*AM.5*AD.19*DY.2019*DM.5*DD.20*A.2*MG.-1*HP.2*FL.3*DSM.1557376509313*RS.1; TAUD=LA-1557370587357-1*RDD-1-2019_05_09*HDD-1-2019_05_19.2019_05_20.1*LD-14460632-2019.5.19.2019.5.20*LG-14460634-2.1.F.; TAUnique=%1%enc%3AmnrKVKxoZ%2FUNSJTzw8g7nz%2BY75sxo05E0eVSasgULgriJ6g91gwMNg%3D%3D; TAReturnTo=%1%%2FHotels%3Fg%3D294265%26----------------------------699496857934629519652157%0D%0AContent-Disposition%3A+form-data%3B+name%3D%22sl_opp_json%22%0D%0A%0D%0A+%7B%7D%0D%0A----------------------------6994968579346295196; BEPIN=%1%16a9adfa69b%3Bweb07c.daodao.com%3A10023%3B; TASSK=enc%3AAFDC5m1hVP55TszJnrOxgvHnD4AC%2Bd2nDnPR%2BySJgZNIsOoQswXP6lktL%2FtXQK3QZeHEPgfzNnUDOP53z4n0%2BFVQFA22Imu%2FkeOvzi7qc6i%2FAO2aWA6d40J1mQLlQ56rcQ%3D%3D; TART=%1%enc%3AQZpLz%2BcEhM419F8Lg6y8XnJkkE7Bx0PIoA1QRnPU5KaXy%2BHktbAQcV9COdpoKOCmb17Xnhe1%2BmY%3D",
    'accept-encoding': "gzip, deflate",
    'Connection': "keep-alive",
    'cache-control': "no-cache"
}

response = requests.request("GET", url, data=payload, headers=headers)

# print(response.text)

import scrapy

page_sel = scrapy.Selector(text=response.text)
hotel_name = page_sel.xpath('//*[@id="HEADING"]//text()').extract()
if len(hotel_name) == 2:
    hotel_name_CH = hotel_name[0]
    hotel_name_EN = hotel_name[1]
else:
    hotel_name_CH, hotel_name_EN = '', ''

comments_count = page_sel.xpath(
    '//span[contains(@class,"reviewCount") and contains(@class,"ui_link")and contains(@class,"level_4")]//text()').extract_first()
comments_count = comments_count.replace('条点评', '')
comments_score = re.findall("alt='(\d\.\d) 分，共 5 分'", response.text)
comments_score = comments_score[0]

page_rank = page_sel.xpath(
    '//span[contains(@class,"header_popularity") and contains(@class,"popIndexValidation")and contains(@class,"ui_link")and contains(@class,"level_4")]/b//text()').extract_first()
page_rank = page_rank.replace('排名第', '')

hotel_location = page_sel.xpath(
    '//div[contains(@class,"ui_column")and contains(@class,"is-12-mobile")and contains(@class,"is-6-tablet")]/div[contains(@class,"sub_content")]//text()').extract()
hotel_location = hotel_location[-1]
print(hotel_location)
print(hotel_name_CH, hotel_name_EN, comments_score, comments_count, page_rank, hotel_location)
