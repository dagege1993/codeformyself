# coding: utf8

import js2py

import logging
import requests

from lxml import etree

from .application import app


@app.task
def crawl(url):
    ta = TripAdvisor(url)
    website = ta.website()
    telephone = ta.telephone()
    contact = {}
    if website:
        contact['website'] = website
    if telephone:
        contact['telephone'] = telephone
    return contact


class TripAdvisor:

    logger = logging.getLogger(__name__)

    def __init__(self, url):
        self.ta_url = url
        self.content = requests.get(url).text
        self.tree = etree.HTML(self.content)

    def website(self):

        js_env = js2py.EvalJs()
        js_env.execute(r'''
            getOffset = function(d) {
                if (d >= 97 && d <= 122) {
                    return d - 61
                }
                if (d >= 65 && d <= 90) {
                    return d - 55
                }
                if (d >= 48 && d <= 71) {
                    return d - 48
                }
                return -1
            };
        ''')
        js_env.execute(r'''
            asdf = function(f) {
                var j = {
                    "": ["&", "=", "p", "6", "?", "H", "%", "B", ".com", "k", "9", ".html", "n", "M", "r", "www.", "h", "b", "t", "a", "0", "/", "d", "O", "j", "http://", "_", "L", "i", "f", "1", "e", "-", "2", ".", "N", "m", "A", "l", "4", "R", "C", "y", "S", "o", "+", "7", "I", "3", "c", "5", "u", 0, "T", "v", "s", "w", "8", "P", 0, "g", 0],
                    q: [0, "__3F__", 0, "Photos", 0, "https://", ".edu", "*", "Y", ">", 0, 0, 0, 0, 0, 0, "`", "__2D__", "X", "<", "slot", 0, "ShowUrl", "Owners", 0, "[", "q", 0, "MemberProfile", 0, "ShowUserReviews", '"', "Hotel", 0, 0, "Expedia", "Vacation", "Discount", 0, "UserReview", "Thumbnail", 0, "__2F__", "Inspiration", "V", "Map", ":", "@", 0, "F", "help", 0, 0, "Rental", 0, "Picture", 0, 0, 0, "hotels", 0, "ftp://"],
                    x: [0, 0, "J", 0, 0, "Z", 0, 0, 0, ";", 0, "Text", 0, "(", "x", "GenericAds", "U", 0, "careers", 0, 0, 0, "D", 0, "members", "Search", 0, 0, 0, "Post", 0, 0, 0, "Q", 0, "$", 0, "K", 0, "W", 0, "Reviews", 0, ",", "__2E__", 0, 0, 0, 0, 0, 0, 0, "{", "}", 0, "Cheap", ")", 0, 0, 0, "#", ".org"],
                    z: [0, "Hotels", 0, 0, "Icon", 0, 0, 0, 0, ".net", 0, 0, "z", 0, 0, "pages", 0, "geo", 0, 0, 0, "cnt", "~", 0, 0, "]", "|", 0, "tripadvisor", "Images", "BookingBuddy", 0, "Commerce", 0, 0, "partnerKey", 0, "area", 0, "Deals", "from", "\\", 0, "urlKey", 0, "'", 0, "WeatherUnderground", 0, "MemberSign", "Maps", 0, "matchID", "Packages", "E", "Amenities", "Travel", ".htm", 0, "!", "^", "G"]
                };
                var e = "";
                for (var d = 0; d < f.length; d++) {
                    var k = f.charAt(d);
                    var g = k;
                    if (j[k] && d + 1 < f.length) {
                        d++;
                        g += f.charAt(d)
                    } else {
                        k = ""
                    }
                    var h = getOffset(f.charCodeAt(d));
                    if (h < 0 || typeof j[k][h] == "String") {
                        e += g
                    } else {
                        e += j[k][h]
                    }
                }
                return e
            };
        ''')    # noqa

        ahref = self.tree.xpath('//div[contains(@class, "website")]/@data-ahref')  # noqa
        if ahref:
            url = 'https://www.tripadvisor.cn' + str(js_env.asdf(ahref[0]))
            resp = requests.head(url)
            if 300 < resp.status_code <= 400:
                return resp.headers.get('Location')
            self.logger.error(
                'Bad response %s, http code %d',
                resp.text,
                resp.status_code
            )

        self.logger.debug('Failed to parse website %s!', self.ta_url)

    def telephone(self):
        get_telephone_script = self.tree.xpath('//div[contains(@class, "phone")]/span/script/text()')  # noqa
        if get_telephone_script:
            script = get_telephone_script[0].split('\n')
            js = [
                line.replace('document.write', 'return ')
                for line in script
                if line != '' and line != '<--'
            ]
            return js2py.eval_js('\n'.join(js))
        self.logger.debug('Failed to parse telephone %s!', self.ta_url)
