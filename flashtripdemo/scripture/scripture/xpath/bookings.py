# coding: utf8
"""
const xpath for booking.com
"""

hotels_id_ren = 'hotel_id: \'(.*?)\''

title_non = '//title/text()'

name_non = '//h2[@id="hp_hotel_name"]/text()'
name_ren = '"name" : "(.*?)",'

LATITUDE_ren = 'b_map_center_latitude = (.*?);'
LONGITUDE_ren = 'b_map_center_longitude = (.*?);'

STAR_ren = 'title="(\d+\.{0,1}\d*)星级酒店'  # noqa
us_url_non = '//link[@hreflang="en-us"]/@href'

STREET_ren = 'streetAddress" : "(.*?),'
locale_ren = 'addressLocality" : "(.*?)"'
city_ren = 'addressRegion" : "(.*?)"'
POSTAL_CODE_ren = 'postalCode" : "(.*?)"'
COUNTRY_ren = 'addressCountry" : "(.*?)"'
ADDRESS_non = '//span[@class="\nhp_address_subtitle\njs-hp_address_subtitle\njq_tooltip\n"]/text()'

around_xpl = '//li[@class="poi-list-item"]weegostring(.)'

SHORT_INTRODUCTION_non = '//meta[@name="twitter:description"]/@content'
INTRODUCTION_sua = '//div[@class="ph-section"]/div/p/span[2]/span[1]|//div[@class="ph-section"]/div/p[@class="ph-item-header"]|//div[@class="ph-section"]/div/p/span/span[contains(@class,"ph-item-")]weegostring(.)'
#DESCRIPTION_sub = '//div[@class="hp_desc_main_content "]|//div[@class="hp_desc_main_content"]|//div[@class=" loc_ltr_for_rtl"]|//span[@class="hp-desc-highlighted"]' # 带有booking上线时间
DESCRIPTION_hotel_sua = '//div[@id="summary"]weegostring(.)'
# PRICE = '//div[@class="price"]/span[contains(@class, "current-price")]/text()' # 未选定日期，不显示价格。

PICTURES_1024_pic = '//div[@data-photoid]/imgweego@src|@data-lazy'# noqa
pictures_1280_pir = 'highres_url: \'(.*?)\''

AMENITIES_xpl = '//div[@class="facilitiesChecklistSection"]weegostring(.)'
landmarks_xpl = '//div[contains(@class,"hp-poi-content-section")]/ul/liweegostring(.)'

SUMMARY_KEY_FACTS_xpl = '//div[@id="checkin_policy"]|//div[@id="checkout_policy"]weegostring(.)'  # noqa
CANCELLATION_POLICY_sub = '//div[@id="cancellation_policy"]'
CHILDREN_POLICY_sub = '//div[@id="children_policy"]'
PET_POLICY_sub = '//div[@class="description"]'
TRAFFIC_TIPS_sua = '//h3[text()="\n邻近机场\n"]/following-sibling::ulweegostring(.)'
restaurant_inn_sub = '//div[@class="restaurant-grid-block"]'
public_transport_options_sua = '//div[@id="public_transport_options"]weegostring(.)'