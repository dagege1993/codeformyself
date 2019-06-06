# coding: utf-8
import logging
from .hotelspro import AsyncHotelsPro
from .get_statics_hotels import HotelBeds
from tasks.utils.database import databases
from web.api.code_to_hotel import code_to_hotelbeds

scripture = databases('scripture')

logger = logging.getLogger(__name__)

async def get_hotel_data(provider, codes):
    if provider == 'hotelspro':
        hotel = await AsyncHotelsPro(scripture).hotel(codes)
        if hotel:
            return hotel
        else:
            logger.warning(f"get {codes} hotelspro hotel failded!")
            return []
    elif provider == 'hotelbeds':
        hotel = await code_to_hotelbeds(codes)
        if hotel:
            return list(hotel.values())
        else:
            logger.warning(f"get {codes} hotelbeds hotel failded!")
            return []
    else:
        logger.info(f"invalid provider! {provider}")
        return []