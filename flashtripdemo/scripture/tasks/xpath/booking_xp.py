CONFIRMATION_NUMBER_VALUES = '//*[@class="responsive_td center_on_mobile"]/p/strong/text()'
CANCELLATION_URL = '//a[@class="#0AB21B-button"]/@href'
HOTEL_NAME = '//*[@class="mg_conf_hotel_preview"]/tr/td/a/b/text()'
HOTEL_URL = '//*[@class="mg_conf_hotel_preview"]/tr[1]/td/a/@href'
TRIP_TYPE = '//*[@class="mg_conf_hotel_preview"]/tr[1]/td/span/text()'
ADDRESS = '//*[@class="mg_conf_hotel_preview"]/tr[2]/td/text()'
ADDRESS_URL = '//*[@class="mg_conf_hotel_preview"]/tr[2]/td/a/@href'
PHONE = '//span[@class="u-phone"]/text()'
STAY = '//*[@class="mg_conf_booking_summary"]/tr[1]/td[2]/text()'
CHECK_IN_DATE_FORMATTED = '//*[@class="mg_conf_booking_summary"]/tr[2]/td[2]/time/@datetime'
CHECK_IN_DATE = '//*[@class="mg_conf_booking_summary"]/tr[2]/td[2]/time/text()'
CHECK_IN_TIME = '//*[@class="mg_conf_booking_summary"]/tr[2]/td[2]/span/text()'
CHECK_OUT_DATE_FORMATTED = '//*[@class="mg_conf_booking_summary"]/tr[3]/td[2]/time/@datetime'
CHECK_OUT_DATE = '//*[@class="mg_conf_booking_summary"]/tr[3]/td[2]/time/text()'
CHECK_OUT_TIME = '//*[@class="mg_conf_booking_summary"]/tr[3]/td[2]/span/text()'
BOOKING_SUMMERY_KEYS = '//table[@class="mg_conf_booking_summary"]/tr/td[1]/b/text()'
BOOKING_SUMMERY_VALUES = '//table[@class="mg_conf_booking_summary"]/tr/td[2]'
PREPAYMENT = '//table[@class="mg_conf_booking_summary"]/tr/td[2]/div/text()'

CANCELLATION_COST = '//table[@class="mg_conf_booking_summary"]/tr/td[2]/ul/li'
PRICE_DETAILS = '//table[@class="mg_conf_price_breakdown"]//b/text()'
PRICE_EXTRA = '//*[@class="mg_conf_price_extra"]/tr/td/text()'

CHANGE_LINKS_KEYS = '//*[@class="mg_conf_mybooking_widget"]/tr[3]/td/table/tr' \
                    '/td/ul/li/a/text()'
CHANGE_LINKS_VALUES = '//*[@class="mg_conf_mybooking_widget"]/tr[3]/td/' \
                      'table/tr/td/ul/li/a/@href'

ROOM_AREA = '//*[@class="mg_conf_room_name_and_description"]/tr/td/text()'

SPECIAL_REQUEST_1 = '//*[@class="mg_conf_special_request"]/' \
                    'tr/td/table/tr/td/text()'
SPECIAL_REQUEST_2 = '//*[@class="mg_conf_special_request"]/tr/td/text()'

IMPORTANT_INFORMATION = '//*[@id="email_body"]/tr/td/table[2]/tr[2]/td/table[' \
                        '8]/tr/td/table/tr/td/table/tr/td/table/tr/td/p/text()'

PAYMENT_FORMS = '//*[@class="mg_conf_payment"]/tr[3]/td/div/text()'

BOOKING_CONDITIONS_KEYS = '//*[@class="mg_conf_hotel_policies"]' \
                          '/tr/td/table/tr/' \
                          'td[@class="responsive_td responsive_key"]/b/text()'
# remove_tags
BOOKING_CONDITIONS_VALUES = '//*[@class="mg_conf_hotel_policies"]/tr/td/table' \
                            '/tr/td[@class="responsive_td responsive_value"]'

CANCELLATION = '//table[@class="mg_conf_reassurance"]' \
               '/tr/td/table/tr[4]/td[2]/text()'