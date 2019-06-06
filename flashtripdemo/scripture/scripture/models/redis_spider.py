from . import BaseModels
from scrapy import Field


class DistributedSpiderModels(BaseModels):
    min_price = Field()
    prices = Field()
    cms_id = Field()


class MatchPrice(BaseModels):
    compair = Field()
    compair_price = Field()
    compair_room_type = Field()
    stage = Field()
    weego_price = Field()
    weego_room_type = Field()
    checkin = Field()
    checkout = Field()
    cms_id = Field()
    meal_type = Field()
    query_time = Field()
    is_package = Field()
    prices = Field()
    hotel_name = Field()
    user_id = Field()
    cancel_policy = Field()
    source = Field()
    user_ip = Field()
    source_type = Field()
    voucher = Field()
    detail_status_code = Field()
    uid = Field()


class CTripPrice(BaseModels):
    prices = Field()
    cms_id = Field()


class TripAdvisor(BaseModels):
    # spider_name = Field()
    hotel_name_ch = Field()
    hotel_name_en = Field()
    hotel_address = Field()
    hotel_tripadvisor_url = Field()
    hotel_booking_url = Field()
    hotel_low_price = Field()
    start_time = Field()
    end_time = Field()
    country_name = Field()
    city_name = Field()
    hotel_desc = Field()
    lost_desc = Field()
    star_level = Field()
    comment_level = Field()
    latitude = Field()
    longitude = Field()
    phone = Field()
    booking_name = Field()
    booking_url = Field()
    hotel_facility = Field()
    room_nums = Field()
    image_url = Field()
    comments = Field()