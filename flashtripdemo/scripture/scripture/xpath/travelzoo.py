# coding: utf8

import re

highlight_container = './/div[@id="theDeal"]/div[@class="deal-details"]/'
highlight_container += 'div[contains(@class, "details-middle")]'

the_deal = './/div[@class="section deal-details-list"]/p/text()'
the_deal2 = highlight_container + '/div[contains(@class, "section")]'

why_love = highlight_container + '/div[contains(@class, "section")]'
why_love += '/h2[contains(text(), "Why We Love It")]/following-sibling::ul'
why_love += '/li/text()'

avalible = './/div[@class="details-right-lower"]/div'
avalible += '/div[@class="box-solid"]/p/text()'

circel = './/div[@id="deal-action-circle"]/div'

kicker = circel + '/h3/text()'
price = circel + '/h2/s/text()'
p_price = circel + '/h2/text()'
external_link = circel + '/a/@href'

included = './/div[@id="theDeal"]/div[3]/div[2]/div[3]/ul/li'

term = './/div[@id="theDeal"]/div[3]/div[2]/div[4]'
policies = highlight_container + '/div[contains(@class, "section")]'
policies += '/h2[contains(text(), "Policies")]/following-sibling::div/p'

rate_summary = '//div[@id="deal-reviews"]/div[contains(@class,"review-intro")]'
rate_summary += '/div[@class="review-container"]/div[@class="review-copy"]'
rate_summary += '/div[@class="headline"]/text()'

review = './/div[@id="deal-reviews"]/div[@class="reviews-macro"]'
review += '/div[contains(@class, "row js-review review")]'

review_req = '//script[@type="text/javascript" and starts-with(normalize-space'
review_req += '(text()), "tzoo.Deal.InitReviews(")]/text()'

currency = re.compile('[^A-Z]([A-Z]{3})[^A-Z]')

overview = highlight_container + '/div[contains(@class, "section")]'
overview += '/h2[contains(text(), "Overview")]/following-sibling::p/text()'
