# coding: utf8

# from yarl import URL
from w3lib.html import remove_tags

from scrapy import Item, Field
from scrapy.loader.processors import TakeFirst, MapCompose, Identity
from . import BaseModels

# from scripture.xpath import hotels as xp


class Hotels(BaseModels):
    hotels_id = Field(output_processor=TakeFirst())
    statics_hotels_id = Field(output_processor=TakeFirst())
    statics_hotels_supplier = Field(output_processor=TakeFirst())
    url = Field(output_processor=TakeFirst())
    us_url = Field(output_processor=TakeFirst())
    title = Field(
        input_processor=MapCompose(lambda t: t.split('|')[0]),
        output_processor=TakeFirst()
    )
    name = Field(output_processor=TakeFirst())
    locale = Field(output_processor=TakeFirst())
    address = Field(
        input_processor=Identity(),
        output_processor=TakeFirst()
    )
    address_text = Field(output_processor=TakeFirst())
    price = Field(output_processor=TakeFirst())
    city = Field(output_processor=TakeFirst())
    star = Field(serializer=int, output_processor=TakeFirst())
    country = Field(output_processor=TakeFirst())
    telephone = Field(output_processor=TakeFirst())
    rating = Field(output_processor=TakeFirst())
    tripadvisor = Field(output_processor=TakeFirst())
    landmarks = Field(input_processor=MapCompose(remove_tags))
    traffic_tips = Field(input_processor=MapCompose(remove_tags))
    geocode = Field()
    longitude = Field(output_processor=TakeFirst())
    latitude = Field(output_processor=TakeFirst())
    notice = Field(output_processor=TakeFirst())
    #     'term': Field(input_processor=MapCompose(remove_tags)),
    #     'alias': Field(input_processor=MapCompose(remove_tags)),
    #     'mandatory fees': Field(input_processor=MapCompose(remove_tags)),
    #     'optional fees': Field(input_processor=MapCompose(remove_tags)),
    # }
    in_store_service_facilities = Field(
        input_processor=Identity(),
        output_processor=TakeFirst()
    )
    room_service_facilities = Field(
        input_processor=Identity(),
        output_processor=TakeFirst()
    )

    summary = Field(output_processor=TakeFirst())

    amenities = Field(input_processor=MapCompose(remove_tags))

    for_families = Field(input_processor=MapCompose(remove_tags))

    around = Field(input_processor=MapCompose(remove_tags))

    pictures = Field()

    short_introduction = Field(
        input_processor=MapCompose(remove_tags),
        output_processor=TakeFirst()
    )
