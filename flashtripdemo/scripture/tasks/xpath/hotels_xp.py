# base information
CONFIRM_NUMBER = '//*[@id="booking-summary-confirmation-number"]/text()'
CHECK_IN_DATE = '//*[@id="booking-summary-check-in-date"]/text()'
CHECK_IN_TIME = '//*[@id="booking-summary-check-in-time"]/text()'
CHECK_OUT_DATE = '//*[@id="booking-summary-check-out-date"]/text()'
CHECK_OUT_TIME = '//*[@id="booking-summary-check-out-time"]/text()'
STAY = '//*[@id="booking-summary-your-stay"]/text()'
CANCELLATION = '//*[@id="booking-summary-short-cancellation-policy"]/text()'
# COST = '//*[@id="hotel-booking-summary-container"]/tbody/tr[10]/td/table/tbody/tr/td[2]/strong/text()'

# hotel details
NAME = '//*[@id="hotel-summary-hotel-name"]/text()'
ADDRESS = '//table[@id="hotel-details-container"]/tr/td[@class="text-cell"]/text()'
TELEPHONE = '//*[@id="hotel-details-container"]/tr/td[@class="text-cell"]/span/text()'
IMPORTANT_NOTICE = '//*[@id="sci_section_30_182_193"]/text()'
REQUIRED = '//*[@id="hotel-details-container"]/tr[@class="required-at-check-in-block"]/td/table/tr/td[@class="responsive right"]/ul/li/text()'

# room details
ROOM_ALL = '//*[@id="room-details-container"]/tr/td/table/tr/td[@class="responsive right"]/text()'
ICON_EXPLANATION = '//*[@id="room-details-container"]/tr[5]/td/table/tr/td[2]/table[1]/tr/td[2]/text()'
ROOM_1 = '//*[@id="room-details-container"]/tr[2]/td/table/tr/td[2]/text()'
ROOM_2 = '//*[@id="room-details-container"]/tr[2]/td/table/tr/td[2]/span/text()'
PREFERENCE = '//*[@id="room-details-container"]/tr[3]/td/table/tr/td[2]/span/text()'
NOTE = '//*[@id="room-details-container"]/tr[4]/td/table/tr/td[2]/div/text()'
FACILITIES_KEYS = '//*[@id="room-details-container"]/tr/td/table/tr/td[@class="responsive right"]/b/text()'
# FACILITIES_VALUES = '//*[@id="room-details-container"]/tr/td/table/tr/td[@class="responsive right"]/text()'
# ROOM_DETAILS = '//*[@id="room-details-container"]/tr/td/table/tr/td[@class="responsive right"]/text()'

# payment details
PRICE = '//table[@id="payment-details-container"]/tr[@class="perroom-pernight-row mobile-proportion"]/td/table/tr/td[2]/text()'
COST = '//table[@id="payment-details-container"]/tr[@class="total-hotel-price-line mobile-proportion"]/td/table/tr/td[2]/text()'


# cancellation policy
CANCELLATION_POLICY_1 = '//*[@id="cancellation-policy"]/ul/li/text()'
CANCELLATION_POLICY_2 = '//*[@id="cancellation-policy"]/text()'
