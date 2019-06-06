# coding: utf8
"""
const xpath for booking.com
"""
ROOMS_BASE_NODE = '//*[@id="maxotel_rooms"]/tbody'
INFO_PAGES = './/tr[@class="extendedRow sold\n"]'
ORDER_PAGES = './/tr[@class="odd"]|.//tr[not(@class)]'

NAMES_EN = "//a[@data-room-name-en]/@data-room-name-en"
NAMES_CN = "//a[@data-room-name-en]/text()"

ROOM_IMAGE = './/img[@alt="这间客房的照片"]/@data-lazy'
ROOM_SIZE = './/div[@data-name-en="roomsize"]/text()'
ROOM_OCCUPANCY_INFO = ".//span[@title]/@title"
ROOM_BED_TYPE = './/div[@class="bed-types-wrapper\n"]'
ROOM_DESC = ".//p/text()"
ROOM_FACILITIES = './/li[@class="hp_rt_lightbox_facilities__list__item"]/text()'

INTRODUCTION = '//div[@id="summary"]'
LANDMARKS = '//div[contains(@class,"landmarks")]/ul/li'

MAIN_FACILITIES = '//div[@class="important_facility "]/text()'
FACILITIES = '//div[@class="facilitiesChecklist"]'

ORI_HOTEL_NAME = '//h2[@id="hp_hotel_name"]/text()'
HOTEL_ADDRESS = '//span[@class="\nhp_address_subtitle\njs-hp_address_subtitle\njq_tooltip\n"]/text()'

POLICES = '//*[@id="hotelPoliciesInc"]'
CONTENT = '//*[@id="hp_important_info_box"]/div[1]/div/text()'
CARDS = '//button[@aria-label][@role="img"]/@aria-label'

PRICES_TABLE_TR = '//div[@class="roomArea"]/form[@id="hprt-form"]/table/tbody/tr[@data-et-view]'
PRICES_FROM = '//div[@id="b_availableRooms"]//form[@id="room_select_form"]'
ROOM_OCCUPANCY = '//td[starts-with(@class,"hprt-table-cell hprt-table-cell-occupancy")]//span/text()'
ROOM_TYPE = '//span[@class="hprt-roomtype-icon-link "]//text()'
ROOM_PRICE = '//div[@class="hprt-price-price "]/span/text()'
ROOM_PRICE_TAX = '//div[@class="hprt-price-price "]/following-sibling::*[1]/text()'
ROOM_POLICIES = '//td[starts-with(@class,"hprt-table-cell hprt-table-cell-conditions")]//ul//text()'
ROOM_SOLD_OUT = '//span[@class="important_text"]/div/text()'
