# coding: utf-8
"""Created by LiuHao
"""

from lxml import etree
from w3lib.html import remove_tags

from tasks.utils.html import take_first
from tasks.utils.html import take_last
from tasks.utils.html import strip_list
from tasks.utils.html import strip_str
from tasks.utils.html import unpack
from tasks.utils.html import remove_space
from tasks.utils.time import DateTime
from tasks.utils.time import to_timezone
from tasks.xpath import expedia_xp

from tasks.parsers import HotelOrderParser


class ExpediaHotelParser(HotelOrderParser):

    """Hotel Expedia.com"""

    @classmethod
    def validate(cls, sender, subject, snippet):
        # TODO(songww): validate
        pass

    def _parse(self):
        result = self._order
        links = self._etree.xpath(expedia_xp.LINK)
        if links and len(links) == 2:
            result['hotel_link'] = links[0]
            result['map_link'] = links[1]
        else:
            self.logger.warning(
                'hotel and map links is empty %s', self._message_id
            )

        tel_fax = take_first(self._etree, expedia_xp.HELP)
        if tel_fax:
            if 'Fax' in tel_fax:
                result['telephone'] = tel_fax.split(', Fax: ')[0].split(': '
                                                                        )[-1]
                result['fax'] = tel_fax.split(':')[-1].strip()
            else:
                result['telephone'] = tel_fax.split(': ')[-1]
        else:
            self.logger.error('telephone is empty %s', self._message_id)

        hotel_name = strip_str(take_first(self._etree, expedia_xp.NAME))
        if hotel_name:
            result['hotel_name'] = hotel_name
        else:
            self.logger.error('hotel_name is empty %s', self._message_id)

        address = strip_str(take_first(self._etree, expedia_xp.ADDRESS))
        if address:
            result['address'] = address
        else:
            self.logger.error('address is empty %s', self._message_id)

        reservation_date = strip_str(
            take_first(self._etree, expedia_xp.RESERVATION_DATE)
        )
        if reservation_date:
            check_in_date, check_out_date = unpack(
                reservation_date.split(' - ')
            )
        else:
            check_in_date = check_out_date = ''
            self.logger.error(
                'reservation_date_raw is empty %s', self._message_id
            )
        if check_out_date and check_in_date:
            result['check_in_date'] = check_in_date
            result['check_out_date'] = check_out_date
            tz = to_timezone(address)
            # date format is unsure
            check_in_date_formatted = DateTime(
                check_in_date,
                'MMM D, YYYY'
            ) \
                .tz_to_datetime(tz)
            if check_in_date_formatted:
                result['check_in_date_formatted'] = check_in_date_formatted
            check_out_date_formatted = DateTime(
                check_out_date,
                'MMM D, YYYY'
            ) \
                .tz_to_datetime(tz)
            if check_out_date_formatted:
                result['check_out_date_formatted'] = check_out_date_formatted

        confirm_number = strip_str(
            take_first(self._etree, expedia_xp.COMFIRM_NUMBER)
        )
        if confirm_number:
            result['confirm_code'] = confirm_number
        else:
            self.logger.error('confirm_number is empty %s', self._message_id)

        reservation_time = strip_list(
            self._etree.xpath(expedia_xp.CHECK_IN_OUT_TIME)
        )
        if reservation_time:
            check_in_time, check_out_time = unpack(reservation_time)
        else:
            check_out_time = check_in_time = ''
            self.logger.error('reservation_time is empty %s', self._message_id)
        if check_in_time and check_out_time:
            result['check_in_time'] = check_in_time
            result['check_out_time'] = check_out_time

        guest = strip_list(self._etree.xpath(expedia_xp.GUEST))
        guest_name = guest[1].split('for '
                                    )[-1] if guest and len(guest) > 1 else ''
        if guest_name:
            result['guest_name'] = guest_name
        else:
            self.logger.error('guest_name is empty %s', self._message_id)
        room = strip_list(self._etree.xpath(expedia_xp.ROOM))
        room_type = room.pop(0) if room and len(room) >= 1 else ''
        if room_type:
            result['room_type'] = room_type
        else:
            self.logger.error('room_type is empty %s', self._message_id)
        if room:
            result['included_amenities'] = [remove_space(i) for i in room]
        else:
            self.logger.error(
                'included_amenities is empty %s', self._message_id
            )

        room_request = strip_list(self._etree.xpath(expedia_xp.ROOM_REQUEST))
        if len(room_request) > 1:
            result['bed_type'] = room_request.pop(1)
        else:
            self.logger.error('bed_type is empty %s', self._message_id)
        if len(room_request) > 1:
            result['room_tips'] = room_request[1:]
        else:
            self.logger.error('room_tip is empty %s', self._message_id)

        price = strip_str(take_last(self._etree, expedia_xp.PRICE))
        if price:
            result['price'] = price
        else:
            self.logger.error('price is empty %s', self._message_id)

        total = strip_str(take_first(self._etree, expedia_xp.TOTAL))
        if total:
            result['total_cost'] = ' '.join(remove_space(total).split(' ')[1:])
        else:
            self.logger.error('price total is empty %s', self._message_id)

        price_des = strip_str(take_last(self._etree, expedia_xp.PRICE_DETAILS))
        if price_des:
            result['price_tips'] = [price_des]
        else:
            self.logger.error('price describe is empty %s', self._message_id)

        taxes = strip_str(take_last(self._etree, expedia_xp.TAXES))
        if taxes:
            result['taxes_fee'] = strip_str(taxes.split(':')[-1])
        else:
            self.logger.warning('taxes is empty %s', self._message_id)

        rules = strip_list(self._etree.xpath(expedia_xp.RULES))
        if rules:
            result['notice'] = [i for i in rules if '.' in i]
        else:
            self.logger.error('notice is empty %s', self._message_id)

        additional_hotel_fee = take_first(
            self._etree, expedia_xp.ADDITIONAL_HOTEL_FEE
        )
        if additional_hotel_fee is not None:
            additional_hotel_fee = strip_list(
                remove_tags(etree.tostring(additional_hotel_fee))
                .replace('&#13;', '').split('\n')
            )
            if len(additional_hotel_fee) > 1:
                result['additional_hotel_fee'] = additional_hotel_fee[1:]
        else:
            self.logger.warning(
                'additional_hotel_fee is empty %s', self._message_id
            )

        check_in_policy = strip_list(
            self._etree.xpath(expedia_xp.CHECK_IN_POLICY)
        )
        if check_in_policy:
            result['check_in_policies'] = check_in_policy[1:]
        else:
            self.logger.warning('policies is empty %s', self._message_id)
        return result
