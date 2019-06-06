# coding: utf-8

from tasks.utils.html import take_first
from tasks.utils.html import strip_list
from tasks.utils.html import strip_str
from tasks.utils.html import remove_space

from tasks.utils.time import to_timezone
from tasks.utils.time import DateTime
from tasks.xpath import wyndham_xp as wdm_xp

from tasks.parsers.order_parser import HotelOrderParser
from tasks.errors.parse_error import MissingColumnError


class WyndhamParser(HotelOrderParser):

    """wyndham.com
    """
    name_dict = {
        'Best Available Rate:': 'price',
        'Tax': 'taxes_fee',
        'Total for Stay': 'total_cost'
    }

    @classmethod
    def validate(cls, sender: str, subject: str, snippet: str) -> bool:
        if not sender.endswith('wyndhamhotelgroup.com'):
            return False
        if 'Your reservation confirmation' not in subject:
            return False

        if 'Your reservation confirmation' not in snippet:
            return False

        return True

    def _parse(self):
        self._order.set(
            'guest_name', take_first(self._etree, wdm_xp.GUEST_NAME)
        )
        self._order['confirm_code'] = take_first(
            self._etree, wdm_xp.CONFIRM_NUM
        )
        if not self._order['confirm_code']:
            raise MissingColumnError('confirm_code', self._message_id)

        self._order['hotel_name'] = take_first(self._etree, wdm_xp.HOTEL_NAME)
        if not self._order['hotel_name']:
            raise MissingColumnError('hotel_name', self._message_id)

        address = strip_list(self._etree.xpath(wdm_xp.ADDRESS))
        if not address:
            raise MissingColumnError('address and telephone', self._message_id)

        self._order['telephone'] = address.pop().strip('Phone: ')
        self._order['address'] = remove_space(', '.join(address))
        if not (self._order['telephone'] and self._order['address']):
            raise MissingColumnError('address or telephone', self._message_id)

        self._order.set(
            'hotel_link', take_first(self._etree, wdm_xp.HOTEL_LINK)
        )
        self._order.set('email', take_first(self._etree, wdm_xp.EMAIL))
        self._order.set(
            'modify_link', take_first(self._etree, wdm_xp.MODIFY_LINK)
        )
        self._order.set(
            'cancellation_link', take_first(self._etree, wdm_xp.CANCEL_LINK)
        )

        reservation = strip_list(self._etree.xpath(wdm_xp.RESERVATION))
        if len(reservation) < 5:
            raise MissingColumnError('reservation', self._message_id)
        self._order.set('room_tips', strip_list(reservation[0].split('\n')))
        self._order.set('number_of_rooms', reservation[1].split(';')[0])
        self._order.set('number_of_nights', reservation[1].split(';')[1])
        self._order.set('number_of_guests', reservation[2])

        check_in = reservation[3].split(' ')
        self._order['check_in_date'] = check_in.pop(0)
        self._order['check_in_time'] = ' '.join(check_in)
        if not (self._order['check_in_date'] and self._order['check_in_time']):
            raise MissingColumnError('check_in', self._message_id)

        checkout = reservation[4].split(' ')
        self._order['check_out_date'] = checkout.pop(0)
        self._order['check_out_time'] = ' '.join(checkout)
        if not (
            self._order['check_out_date'] and self._order['check_out_time']
        ):
            raise MissingColumnError('checkout', self._message_id)

        tz = to_timezone(self._order['address'])
        self._order['check_in_date_formatted'] = DateTime(
            self._order['check_in_date'], 'MM/DD/YYYY'
        ).tz_to_datetime(tz)
        self._order['check_out_date_formatted'] = DateTime(
            self._order['check_out_date'], 'MM/DD/YYYY'
        ).tz_to_datetime(tz)
        if not (
            self._order['check_in_date_formatted'] and
            self._order['check_out_date_formatted']
        ):
            raise MissingColumnError(
                'check_in_out_date_formatted', self._message_id
            )

        price = self._etree.xpath(wdm_xp.PRICE)
        if price:
            for item in price:
                name = strip_str(take_first(item, './td[1]/text()'))
                value = strip_str(take_first(item, './td[2]/text()'))
                currency = strip_str(take_first(item, './td[2]/span/text()'))
                if name in self.name_dict:
                    self._order[self.name_dict[name]] = value + currency
                else:
                    self.logger.warning(
                        'price %s is %s %s', name, value, self._message_id
                    )

        other_info = strip_list(self._etree.xpath(wdm_xp.OTHER_INFO))
        for info in other_info:
            if info.startswith('Cancellation Policy'):
                self._order.set(
                    'cancellation_policies',
                    info.strip('Cancellation Policy: ').split(';')
                )
            elif info.startswith('Payment Method: '):
                self._order.set('payment_card', info.strip('Payment Method: '))
            else:
                self.logger.warning(
                    'other information %s %s', info, self._message_id
                )

        return self._order
