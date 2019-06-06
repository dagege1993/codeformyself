from scrapy import Field
from scrapy.loader.processors import TakeFirst, Identity
from . import BaseModels


class Booking(BaseModels):

    name = Field(output_processor=TakeFirst())
    address = Field(
        input_processor=Identity(),
        output_processor=TakeFirst()
    )
    introduction = Field(
        output_processor=TakeFirst()
    )
    rooms = Field()
    polices = Field()
    attractions = Field()
    facilities = Field()
    all_facilities = Field()
    gallery = Field()
    city_name = Field()
    name_en = Field(
        output_processor=TakeFirst()
    )
    bk_url = Field(
        output_processor=TakeFirst()
    )
    capture_urls_id = Field()
