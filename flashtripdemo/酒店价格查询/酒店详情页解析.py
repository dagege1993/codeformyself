with open('/Users/huangjack/PycharmProjects/codeformyself/flashtripdemo/酒店价格查询/酒店详情页.html', 'r') as f:
    text = f.read()
# print(text)
import scrapy

page_sel = scrapy.Selector(text=text)
result = page_sel.xpath(
    '//div[contains(@class,"is-6-mobile")and contains(@class,"ui_column")]//div[@class="textitem"]//text()').extract()
print(result)

# 尝试解析图片
re.findall('"mediaWindow": ')
