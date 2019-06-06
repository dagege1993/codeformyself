import requests

url = "https://www.tripadvisor.cn/Lvyou"

payload = ""
headers = {
    'User-Agent': "PostmanRuntime/7.11.0",
    'Accept': "*/*",
    'Cache-Control': "no-cache",
    'Postman-Token': "aafade4f-8903-4d80-9eeb-547ace07df24,580441fd-2b59-4d73-97a1-997fad6bf4e7",
    'Host': "www.tripadvisor.cn",
    'accept-encoding': "gzip, deflate",
    'Connection': "keep-alive",
    'cache-control': "no-cache"
}

response = requests.request("GET", url, data=payload, headers=headers)

# print(response.text)

# 解析首页获取亚洲以及对应的目的地
import scrapy
import re

page_sel = scrapy.Selector(text=response.text)
results = page_sel.xpath('//*[@id="tab-body-wrapper-ipad"]//li/a').extract()
for result in results:
    city_name = re.findall('>(.*?)<', result)[0]
    city_url = re.findall('href="(.*?)"', result)[0]  # 城市首页URL
    city_id = re.findall('data-pid="(.*?)"', result)[0]
    print(city_name, city_url, city_id)
    # 需要的是酒店URL
    city_hotel_url = city_url.replace('Vacations', 'Hotels').replace('Tourism', 'Hotels')
    # print(city_hotel_url)
    # 到列表页获取最大页面数
    city_hotel_url = 'https://www.tripadvisor.cn' + city_hotel_url
    print(city_hotel_url)
    city_hotel_url = 'https://www.tripadvisor.cn/Hotels-g186591-Ireland-Hotels.html'
    response = requests.get(city_hotel_url)
    page_sel_list = scrapy.Selector(text=response.text)
    # 需要解析详情页的链接
    hotel_lists = page_sel_list.xpath(
        '//div[contains(@class,"prw_rup") and contains(@class,"prw_meta_hsx_listing_name")and contains(@class,"listing-title")]//a/@href').extract()
    for hotel in hotel_lists:
        hotel_url = 'https://www.tripadvisor.cn' + hotel
        print(hotel_url)
    # print(hotel_lists)
    result_list_count = page_sel_list.xpath(
        '//*[@id="taplc_main_pagination_bar_hotels_pagination_links_optimization_0"]//text()').extract()
    if len(result_list_count) > 1:
        print('当前列表页还有下一页')
        max_page_num = result_list_count[-1]  # 取列表的最后一个是最大页面数
        for page_num in range(2, int(max_page_num) + 1):
            print(page_num)
            # 这里把url拼接好后调用抓取函数就行
    print(result_list_count)
    import requests


def get_hotel_list():
    url = "https://www.tripadvisor.cn/Hotels-g294265-Singapore-Hotels.html"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',

    }

    post_data = {
        'sl_opp_json': {},
        'plSeed': '304484723',
        'reqNum': '2',
        'isLastPoll': 'false',
        'paramSeqId': '0',
        'waitTime': '1001',
        'changeSet': '',
        # 'puid': 'XNPTLMCoAS0ABGs1YQQAAADB',

    }

    response = requests.request("POST", url, data=post_data, headers=headers, verify=False)
    print(response.text)

