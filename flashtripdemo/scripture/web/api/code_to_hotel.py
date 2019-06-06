import logging

from . import api_v1
from web.utils.fix_statics_data.get_statics_hotels import HotelBeds
from tasks.supplier_statics import update_hotelbeds
from .formatter_response import rest_result


@api_v1.route("/codes/hotels", methods=["POST", "OPTIONS"])
async def codes_to_hotels(request):
    logger = logging.getLogger(__name__)
    body = request.json
    if not body:
        logger.warning('request without body!')
        return rest_result(
            request,
            {'status': 400, 'errmsg': 'request without body!'}
        )
    hotelbeds_code = []
    for code in body:
        if code['supplier'] == 'hotelbeds':
            hotelbeds_code.append(code['code'])
    hotelbeds_hotels = await code_to_hotelbeds(hotelbeds_code)
    data = {
        'status': 200,
        'hotelbeds': hotelbeds_hotels
    }
    logger.info(f"find_hotels_by_codes request : {body},response:{data}")
    return rest_result(request, data)


async def code_to_hotelbeds(codes):
    logger = logging.getLogger(__name__)
    hotels_by_code = HotelBeds().hotels(code_list=codes)
    logger.debug(f'hotels_by_code:{hotels_by_code}')
    update_hotelbeds.delay(hotels_by_code)
    data = {}
    for index, hotel in enumerate(hotels_by_code):
        key = codes[index]
        data[key] = {}
        if hotel == 500:
            data[key] = '无法从供应商接口查询到此code'
            continue
        data[key]['name'] = hotel["name"]["content"]
        data[key]['address'] = hotel["address"]["content"]
        try:
            data[key]['latitude'] = hotel["coordinates"]["latitude"]
            data[key]['longitude'] = hotel["coordinates"]["longitude"]
        except KeyError:
            pass
        for phone in hotel.get("phones", []):
            if phone["phoneType"].upper().startswith("PHONE"):
                data[key]["phone"] = phone["phoneNumber"]
        data[key]["website"] = hotel.get('web') or ''
        data[key]["city"] = hotel["city"]["content"].title()
        data[key]["postalCode"] = hotel['postalCode']
        facilities = hotel.get('facilities') or ''
        data[key]["facilities"] = len(facilities)
        images = hotel.get('images') or ''
        data[key]["images"] = len(images)
        interestPoints = hotel.get('interestPoints') or ''
        data[key]["interestPoints"] = len(interestPoints)
        rooms = hotel.get('rooms') or ''
        data[key]["rooms"] = len(rooms)
    logger.info(f'原codes信息:{codes},查询结果:{data}')
    return data
