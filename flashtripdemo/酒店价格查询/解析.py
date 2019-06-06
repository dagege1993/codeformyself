text1 = """        <div class="partialMatchInfoContainer "><span class="label">缺少：</span><span class="partialMatchInfo"><span
                class="info strikethrough">4 星级</span><span class="info strikethrough">5 星级</span></span></div>


"""
import scrapy

# selector_response = scrapy.Selector(text=text)

# LOST_DESC = selector_response.xpath('//*[@class="partialMatchInfoContainer"]').extract()

selector_response = scrapy.Selector(text=text1)

results = selector_response.xpath('//*[@class="partialMatchInfoContainer "]//text()').extract()

print(results)
