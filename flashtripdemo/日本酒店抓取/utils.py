import re

with open('/Users/huangjack/PycharmProjects/codeformyself/flashtripdemo/日本酒店抓取/有住宿设备酒店咨询.html', 'r') as f:
    # with open('/Users/huangjack/PycharmProjects/codeformyself/flashtripdemo/日本酒店抓取/有入住政策酒店详情页.html', 'r') as f:
    detail_response_text = f.read()

import scrapy

# print(result)
page_sel = scrapy.Selector(text=detail_response_text)
facility_list = page_sel.xpath("//*[@class='facility_info_tables']").extract()
del (facility_list[0])
facility_desc_lis = []
for i in (facility_list):
    if '建筑物构造' not in i and '其他可接受信用卡种类' not in i:
        page_lisgt = scrapy.Selector(text=i)
        facility_desc = page_lisgt.xpath('*//table/tr/th/text()').extract()
        facility_desc = (','.join(facility_desc).strip())
        facility_desc_lis.append(facility_desc)
print(facility_desc_lis)
facility_desc_lis = [facility_desc.strip().replace('\n', '') for facility_desc in facility_desc_lis]
facility_dict = {'facility_title': '住宿设施资讯', 'facility_desc': facility_desc_lis}
print(facility_dict)
image_list = re.findall('https:\/\/.*?jpg', detail_response_text)
policy_children = page_sel.xpath('//*[@style="display:inline;"]/text()').extract()
policy_children = [policy.replace('\n', '').strip() for policy in policy_children]
print(policy_children)

if '有关儿童入住规定:接受儿童入住' in policy_children and '有关儿童入住规定:不接受儿童入住' in policy_children:
    policy_children = ['部分房型不接受儿童']
else:
    policy_children = policy_children[0]
print(policy_children)
print(image_list)
accss_info = page_sel.xpath('*//p[@class="hotelinfo__access"]/a/text()').extract_first()
name_info = page_sel.xpath('*//h1[@class="hotelinfo__name"]/span/text()').extract_first()
fa_info = page_sel.xpath('*//ul[@id="hotel_contents_0_IconUl"]/li/text()').extract()
desc = page_sel.xpath('*//p[@id="hotel_contents_0_SalesPointParagraph"]/text()').extract_first()
city = page_sel.xpath('//*[@itemtype="http://data-vocabulary.org/Breadcrumb"]/li/a/text()').extract()
city = city[2]
policy = page_sel.xpath('//*[@id="hotel_contents_0_EmergencyInformation"]/dl/dd/text()').extract()
print(accss_info, name_info, fa_info, desc)
print(city)
print(policy)

with open('/Users/huangjack/PycharmProjects/codeformyself/flashtripdemo/日本酒店抓取/评论页解析.html', 'r') as f:
    comment_response_text = f.read()
comment_response_text = scrapy.Selector(text=comment_response_text)
comment_list = comment_response_text.xpath('//*[@class="reviewModule"]').extract()
comment_list = comment_list[0:5]  # 不管多少,最多取前面五条评论
comment_dict_list = []
for comment in comment_list:
    comment_dict = {}
    comment = scrapy.Selector(text=comment)
    name = comment.xpath('//*[@class="name"]/text()').extract_first()
    star = comment.xpath('//*[@class="reviewStars"]//text()').extract_first()
    user_comment = comment.xpath('//*[@class="comment"]//text()').extract_first()
    if user_comment is None:
        pass
    else:
        user_comment = user_comment.replace('/n', '').strip()
    time = comment.xpath('/html/body/div/table/tbody/tr[1]/td[1]/text()').extract_first()
    locale = '中文'
    comment_dict['name'] = name
    comment_dict['star'] = star
    comment_dict['user_comment'] = user_comment
    comment_dict['time'] = time
    comment_dict['locale'] = locale
    comment_dict_list.append(comment_dict)
print(comment_dict_list)
