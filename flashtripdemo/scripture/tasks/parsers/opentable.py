# coding: utf-8
"""Create by LiuHao
"""

from tasks.utils.html import take_first
from tasks.utils.html import strip_list
from tasks.utils.html import strip_str
from tasks.utils.html import to_dict
from tasks.utils.html import filter_dict_value
from tasks.utils.time import to_timezone
from tasks.utils.time import DateTime
from tasks.xpath import opentable_xp

from tasks.parsers import RestOrderParser


class OpenTableParser(RestOrderParser):

    @classmethod
    def validate(cls, sender, subject, snippet):
        # TODO(songww): validate
        if not ('opentable.com' in sender and 'Reservations' in sender):
            return False
        if 'Your Reservation Confirmation for' not in subject:
            return False
        if 'OpenTable Reservation confirmed Thanks for using' not in snippet:
            return False
        return True

    def _parse(self):
        result = self._order
        restaurant_name = take_first(self._etree, opentable_xp.NAME)
        if restaurant_name:
            result['restaurant_name'] = restaurant_name
        else:
            self.logger.error('restaurant_name is empty %s', self._message_id)

        address = ', '.join(
            strip_list(self._etree.xpath(opentable_xp.ADDRESS))
        )
        if restaurant_name:
            result['address'] = address
        else:
            self.logger.error('address is empty %s', self._message_id)

        guest_name = take_first(self._etree, opentable_xp.USER_NAME)
        if guest_name:
            result['guest_name'] = guest_name
        else:
            self.logger.error('guest_name is empty %s', self._message_id)

        confirm_number = take_first(
            self._etree, opentable_xp.CONFIRMATION_NUMBER
        )
        if confirm_number:
            result['confirm_code'] = confirm_number
        else:
            self.logger.error('confirm_number is empty %s', self._message_id)

        check_in_datetime = take_first(self._etree, opentable_xp.DATETIME)
        if check_in_datetime:
            result['check_in_datetime'] = check_in_datetime
            tz = to_timezone(address)
            dt = DateTime(check_in_datetime, 'MMMM D, YYYY .. h:mm A')
            check_in_datetime_formatted = dt.tz_to_datetime(tz)
            if check_in_datetime_formatted:
                result['check_in_datetime_formatted'] = \
                    check_in_datetime_formatted
            else:
                self.logger.error(
                    'check_in_datetime_formatted is empty %s', self._message_id
                )
        else:
            self.logger.error(
                'check_in_datetime is empty %s', self._message_id
            )

        tel = take_first(self._etree, opentable_xp.PHONE)
        if tel:
            result['telephone'] = tel
        else:
            self.logger.error('telephone is empty %s', self._message_id)

        title = take_first(self._etree, opentable_xp.PROMOTED_OFFER_TITLE)
        if not title:
            self.logger.warning(
                'promote_offer_title is empty %s', self._message_id
            )
        details = take_first(self._etree, opentable_xp.PROMOTED_OFFER_DETAILS)
        if not details:
            self.logger.warning(
                'promote_offer_details is empty %s', self._message_id
            )
        condition = take_first(
            self._etree, opentable_xp.PROMOTED_OFFER_CONDITIONS
        )
        if not condition:
            self.logger.warning(
                'promote_offer_condition is empty %s', self._message_id
            )
        promote_offer_values = [title, details, condition]
        promote_offer_names = ['title', 'details', 'conditions']
        promote_offer = to_dict(promote_offer_names, promote_offer_values)
        promote_offer = filter_dict_value(promote_offer)
        if promote_offer:
            result['promote_offer'] = promote_offer

        menu = take_first(self._etree, opentable_xp.MENU)
        if menu:
            result['menu_link'] = menu
        else:
            self.logger.warning('menu_link is empty %s', self._message_id)
        direction = take_first(self._etree, opentable_xp.DIRECTION)
        if direction:
            result['map_link'] = direction
        else:
            self.logger.warning('direction_link is empty %s', self._message_id)
        restaurant_link = take_first(self._etree, opentable_xp.NAME_LINK)
        if restaurant_link:
            result['restaurant_link'] = restaurant_link
        else:
            self.logger.warning(
                'restaurant_link is empty %s', self._message_id
            )
        links = self._etree.xpath(opentable_xp.LINK)
        links_name = strip_list(self._etree.xpath(opentable_xp.LINK_NAME))
        name_dict = {
            'Cancel': 'cancellation_link',
            'Modify': 'modify_link',
            'Calendar': 'calendar_link',
            'Share': 'share_link'
        }
        if links and links_name:
            for i, j in zip(links_name, links):
                if i in name_dict.keys():
                    result[name_dict[i]] = j
                else:
                    self.logger.warning('%s is %s %s', i, j, self._message_id)
        else:
            self.logger.error('related_links is empty %s', self._message_id)

        confirmation = '\n'.join(
            self._etree.xpath(opentable_xp.RESTAURANT_CONFIRMATION)
        )
        if confirmation:
            result['restaurant_confirmation'] = confirmation
        else:
            self.logger.warning(
                'restaurant_confirmation is empty %s', self._message_id
            )

        restaurant_details = strip_str(
            take_first(self._etree, opentable_xp.RESTAURANT_DETAILS)
        )
        if restaurant_details:
            result['restaurant_details'] = restaurant_details
        else:
            self.logger.warning(
                'restaurant_details is empty %s', self._message_id
            )

        notice = strip_list(self._etree.xpath(opentable_xp.NOTE))
        if notice:
            result['notice'] = [i.split(': ')[-1] for i in notice]
        else:
            self.logger.warning('notice is empty %s', self._message_id)

        your_special_requirement = strip_list(
            self._etree.xpath(opentable_xp.SPECIAL_NOTE)
        )
        if your_special_requirement:
            result['your_special_requirement'] = your_special_requirement
        else:
            self.logger.info(
                'your_special_requirement is empty %s', self._message_id
            )
        return result
