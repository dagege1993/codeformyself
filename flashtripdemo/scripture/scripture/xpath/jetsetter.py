# coding: utf8

whatoknow = '//div[@class="what-to-know-list"]/h3[contains(text(), '
whatoknow += '"What To Know")]/following-sibling::ul/li/span/text()'

whatwelove = '//div[@class="what-to-know-list"]/h3[contains(text(), '
whatwelove += '"What We Love")]/following-sibling::ul/li/span/text()'

amenities = '//div/h3[contains(text(), "Amenities")]/following-sibling::ul'
amenities += '/li/text()'

overview = '//div[@id="overview"]/div/div/div[@class="editorial-review"]'

howtogethere = '//div[@class="how-to-get-there-info"]/div'
howtogethere += '/div[@class="map-subtext"]/address'
howtogethere1 = '//div[@class="travel-tips"]/address'

travel_tips = '//div[@class="travel-tips"]/span/text()'

latitude = '//meta[@name="place:location:latitude"]/@content'
longitude = '//meta[@name="place:location:longitude"]/@content'

body = '//div[@id="page-product"]'

gallery = '//div[@id="product-gallery"]/div[@class="content"]'

images = gallery + '//a[@class="image-viewer-link"]/div/div/img'

price = gallery + '/div[@class="property-rate-summary"]/div[contains(@class,'
price += '"rate-summary-container")]/div[contains(@class, "pricing")]'
price += '/span[@class="best-available-rate"]/text()'

props = gallery + '/div[@class="property-header"]'

tag = props + '/div[@class="property-market-category"]'
tag += '/div[contains(@class, "market-category"]/text()'

name = props + '/h1[@class="property-title"]/text()'
city_state = props + '/div[@class="property-subtitle"]/text()'

ta_reviews = '//div[@id="reviews"]/div[@class="combined-reviews"]'
ta_reviews += '/div[@class="ta-reviews-container"]/div'

ta_rating = ta_reviews + '/div[@class="ta-review-summary"]'
ta_rating += '/span[@class="overall-rating"]/text()'

ta_url = ta_reviews + '/div[@class="read-all-container"]'
ta_url += '/a[contains(text(), "Read All Reviews")]/@href'
