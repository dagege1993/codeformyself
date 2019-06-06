# coding: utf-8

from tasks.utils.html import take_first
from tasks.utils.html import remove_space
from tasks.utils.html import strip_str
from tasks.utils.html import strip_list
from tasks.utils.time import to_timezone
from tasks.utils.time import DateTime
from tasks.xpath import britishairways_xp as ba_xp

from tasks.parsers import FlightOrderParser
from tasks.errors.parse_error import MissingColumnError


class BritishAirwaysParser(FlightOrderParser):

    """britishairways.com
    """
    name_dict = {
        'Hand baggage': 'hand_baggage_allowance',
        'Checked baggage': 'checked_baggage_allowance',
        'Ticket Number(s)': 'ticket_number',
        'Card Type': 'payment_card_type',
        'Card Holder': 'payment_card_holder',
        'Card Number': 'payment_card_number',
        'Billing Address': 'billing_address',
        'Payment Total': 'total_cost',
        'Payment Date': 'payment_date',
        'IATA Number': 'iata_number',
        'Endorsements': 'endorsements',
        'Fare Details': 'taxes_fee',
        'Fare breakdown': 'fare_summary'
    }

    @classmethod
    def validate(cls, sender, subject, snippet):
        if not (
            sender.strip().startswith('British Airways e-ticket') and
            sender.strip('>').endswith('ba.com')
        ):
            return False

        if not subject.startswith('Your e-ticket'):
            return False

        # TODO(LensHo): 需要用snippet来验证是否需要解析
        print("ba.com snippet: ", snippet)

        return True

    def _parse(self):
        result = self._order
        result['confirm_code'
               ] = strip_str(take_first(self._etree, ba_xp.CONFIRM_CODE))
        if not result['confirm_code']:
            raise MissingColumnError('confirm_code', self._message_id)

        try:
            result['flight_number'] = self._etree.xpath(ba_xp.FLIGHT_NUM)[0]
        except IndexError as e:
            raise MissingColumnError('flight_number', self._message_id) from e

        itinerary = strip_list(self._etree.xpath(ba_xp.ITINERARY))
        if len(itinerary) != 8:
            raise MissingColumnError('itinerary', self._message_id)
        result['depart_date'], result['arrive_date'] = itinerary[::4]
        result['depart_time'], result['arrive_time'] = itinerary[1::4]
        result['depart_city'], result['arrive_city'] = itinerary[2::4]
        result['depart_terminal'] = itinerary[3]
        result['arrive_terminal'] = itinerary[-1]
        tz_dp, tz_ar = to_timezone(itinerary[2]), to_timezone(itinerary[6])
        dp_dt, ar_dt = ' '.join(itinerary[:2]), ' '.join(itinerary[4:6])
        # TODO(LensHo): 小时的格式可能为H
        dt_format = 'd MMM YYYY HH:mm'
        result['depart_datetime_formatted'] = DateTime(dp_dt, dt_format) \
            .tz_to_datetime(tz_dp)

        if not result['depart_datetime_formatted']:
            result.pop('depart_datetime_formatted')
            self.logger.error(
                'depart_datetime_formatted is empty %s', self._message_id
            )

        result['arrive_datetime_formatted'] = DateTime(ar_dt, dt_format) \
            .tz_to_datetime(tz_ar)

        if not result['arrive_datetime_formatted']:
            result.pop('arrive_datetime_formatted')
            self.logger.error(
                'arrive_datetime_formatted is empty %s', self._message_id
            )

        guest = strip_list(self._etree.xpath(ba_xp.GUEST))
        if guest:
            guest = [name for name in guest if name != 'Passenger']
            result['guest_name'] = ', '.join(guest).strip(', ')
            result['guest_names_list'] = guest
        else:
            self.logger.error('guest_name is empty %s', self._message_id)

        baggage_names = strip_list(self._etree.xpath(ba_xp.BAGGAGE_NAMES))
        baggage_values = strip_list(self._etree.xpath(ba_xp.BAGGAGE_VALUES))
        if baggage_names and baggage_values:
            for name, value in zip(baggage_names, baggage_values):
                if name in self.name_dict:
                    result[self.name_dict[name]] = value
                else:
                    self.logger.warning(
                        'baggage information %s is %s', name, value
                    )
        else:
            self.logger.error(
                'baggage_allowance is empty %s', self._message_id
            )

        airline_link = self._etree.xpath(ba_xp.AIRLINE_LINK)
        airline_text = self._etree.xpath(ba_xp.AIRLINE_TEXT)
        if airline_link:
            result['carrier_link'] = airline_link[0]
            result['carrier_name'] = airline_text[0]
            if len(airline_link) >= 2:
                result['trans_airline_link'] = airline_link[1]
                result['trans_airline_name'] = airline_text[1]
        else:
            self.logger.warning('airline name is empty %s', self._message_id)

        result['disability_assistance'] = strip_str(
            take_first(self._etree, ba_xp.DISABILITY_ASSISTANCE)
        )
        if not result['disability_assistance']:
            result.pop('disability_assistance')
            self.logger.warning(
                'disability assistance is empty %s', self._message_id
            )

        payment = self._etree.xpath(ba_xp.PAYMENT)
        if payment:
            for item in payment:
                item = strip_list(item.xpath('./td/text()'))
                if item:
                    if item[0] in self.name_dict:
                        result[self.name_dict[item[0]]] = remove_space(item[1])
                    elif len(item) == 1:
                        result['ticket_number'] = ', '.join([
                            result.get('ticket_number', ''),
                            remove_space(item[0])
                        ])
                    else:
                        self.logger.warning(
                            '%s is %s %s', item[0], item[1], self._message_id
                        )
        else:
            self.logger.error('payment is empty %s', self._message_id)

        result['modify_link'] = take_first(self._etree, ba_xp.CHANGE_LINKS)
        if not result['modify_link']:
            result.pop('modify_link')
            self.logger.error('modify link is empty %s', self._message_id)

        links = self._etree.xpath(ba_xp.LINKS)
        if links:
            result['related_links'] = []
            for item in links:
                name = take_first(item, './text()')
                link = take_first(item, './@href')
                if name and link:
                    result['related_links'].append({
                        'name': name,
                        'link': link
                    })
            if not result:
                result.pop('related_links')
                self.logger.error(
                    'related_links is empty %s', self._message_id
                )
        else:
            self.logger.error('related_links is empty %s', self._message_id)

        return result
