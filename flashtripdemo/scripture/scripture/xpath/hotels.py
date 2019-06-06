# coding: utf8
"""
const xpath for hotels.cn
"""

TITLE = '//head/meta[@name="title"]/@content'

NAME = '//h1/text()'

POSITION = '//head/meta[@name="geo.position"]/@content'
LATITUDE = '//span[@itemprop="geo"]/meta[@itemprop="latitude"]/@content'
LONGITUDE = '//span[@itemprop="geo"]/meta[@itemprop="longitude"]/@content'

STAR = '//div[@class="vcard"]/span[contains(@class,"star-rating-text")]/text()'  # noqa
EN_US_URL = '//head/link[@hreflang="en-US"]/@href'

ADDRESS_STREET = '//span[@class="property-address"]/span[@class="postal-addr"]/span[@class="street-address"]/span/text()'
ADDRESS_LOCALITY = '//span[@class="property-address"]/span[@class="postal-addr"]/span[@class="locality"]/span/text()'
ADDRESS_REGION = '//span[@class="property-address"]/span[@class="postal-addr"]/span[@class="region"]/span/text()'
ADDRESS_POSTAL_CODE = '//span[@class="property-address"]/span[@class="postal-addr"]/span[@class="postal-code"]/span/text()'
ADDRESS_COUNTRY = '//span[@class="property-address"]/span[@class="postal-addr"]/span[@class="country-name"]/text()'
ADDRESS_INFO = '//script[@id="pdp-linked-data"]/text()'
ADDRESS = '//span[@class="postal-addr"]/text()'
EN_ADDRESS = '//span[@class="postal-addr"]//span/text()'

TELEPHONE = '//span[@id="hd_property_info_tfn"]/text()'

# SHORT_INTRODUCTION = '//div[@class="tagline"]/b | p/text()'
SHORT_INTRODUCTION = '//div[@class="tagline"]/b/text()|//div[@class="tagline"]/p/text()'
DESCRIPTION = ''

PRICE = '//div[@class="price"]/span[contains(@class, "current-price")]/text()'
PICTURES = '//div[@id="carousel-container"]/div[contains(@class, "canvas")]/ul/li'  # noqa

AMENITIES = '//div[@id="overview-section-4"]/ul/li'
FOR_FAMILIES = '//div[@id="overview-section-5"]/ul/li'
AROUND = '//div[@id="overview-section-6"]/ul/li'


SUMMARY_KEY_FACTS = '//div[contains(@class, "key-facts-container")]/div[@class="info-box"]/ul/li'  # noqa
SUMMARY_TRAVELLING = '//div[contains(@class, "travelling-container")]/div[@class="info-box"]/ul/li'  # noqa
SUMMARY_TRANSPORT = '//div[contains(@class, "transport-container")]/div[@class="info-box"]/ul/li'  # noqa

CN_IN_STORE_SERVICE_FACT = '//h2[text()="店内服务设施"]/following-sibling::div/div[@class="fact-sheet-table-row"]'  # noqa
CN_ROOM_SERVICE_FACT = '//h2[text()="客房服务设施"]/following-sibling::div/div[@class="fact-sheet-table-row"]'  # noqa
EN_IN_STORE_SERVICE_FACT = '//h2[text()="In the hotel"]/following-sibling::div/div[@class="fact-sheet-table-row"]'  # noqa
EN_ROOM_SERVICE_FACT = '//h2[text()="In the room"]/following-sibling::div/div[@class="fact-sheet-table-row"]'  # noqa
SERVICE_FACT_TITLE = '/div[@class="fact-sheet-table-header"]/text()'
SERVICE_FACT_CELL = '/div[@class="fact-sheet-table-cell"]/ul/li/text()'

CN_ALIAS = '//div[@class="small-print-section"]/h3[text() = "别称"]/following-sibling::ul/li'  # noqa
CN_TERM = '//div[@class="small-print-section"]/h3[text() = "政策"]/following-sibling::p'  # noqa
CN_MANDATORY_FEES = '//div[@class="small-print-section"]/h3[text() = "强制性费用"]/following-sibling::ul/li'  # noqa
CN_OPTIONAL_FEES = '//div[@class="small-print-section"]/h3[text() = "其他可选项"]/following-sibling::p'  # noqa

EN_ALIAS = '//div[@class="small-print-section"]/h3[text() = "Also known as"]/following-sibling::ul/li'  # noqa
EN_TERM = '//div[@class="small-print-section"]/h3[text() = "Policies"]/following-sibling::p'  # noqa
EN_MANDATORY_FEES = '//div[@class="small-print-section"]/h3[text() = "Mandatory fees"]/following-sibling::ul/li'  # noqa
EN_OPTIONAL_FEES = '//div[@class="small-print-section"]/h3[text() = "Optional extras"]/following-sibling::p'  # noqa

LANDMARKS = '//div[@class="whats-around-content-landmarks-transport"]//ul[@class="top-spots-list"]/li/text()|//div[@class="whats-around-content-landmarks-transport"]//ul[@class="landmark-list"]/li/text()'  # noqa
TRAFFIC_TIPS = '//div[@class="whats-around-content transport"]/ul/li'

ROOMS_LIST = '//div[@id="rooms-and-rates"]/ul[@class="rooms"]/li'
ROOM_NAME = '/div[@class="room-info"]/h3/text()'
ROOM_INFO = '/div[@class="room-info"]/div[@class="room-images-and-info"]/div[@class="room-and-hotel-info"]' # noqa
ROOM_SIZE = ROOM_INFO + '/ul[@class="room-amenities"]/li[@class="room-size"]/span'  # noqa
ROOM_OCCUPANCY = ROOM_INFO + '/div[@class="occupancy"]/span[@class="occupancy-info"]' # noqa
ROOM_BEDS = ROOM_INFO + '/div[@class="room-beds-info"]/h4/text()'
ROOM_BEDS_SIZE = ROOM_INFO + '/div[@class="room-beds-info"]/h4/span/text()'
ROOM_EXTRA_BEDS = ROOM_INFO + '/div[@class="room-beds-info"]/p/span'
ROOM_DESC = '/div[@class="additional-room-info"]'
ROOM_DESCRIPTION = ROOM_DESC + '/div[contains(@class, "room-description")]/ul'
ROOM_AMENITIES = ROOM_DESC + '/div[contains(@class, "room-details")]/ul/li/text()'  # noqa
HCOM_CLIENT_DATA = '//script[starts-with(text(), "var hcomi18nData")]/text()'
ROOM_TYPE_CODE = '/div[@class="rateplans"]//input[@name="bookingRequest.roomTypeCode"]/@value'  # noqa
