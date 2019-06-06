# coding: utf8

# Standard Library
import re
import logging
from html import unescape

# Non Standard Library
from yarl import URL
import requests
from simhash import Simhash
from sanic.response import json

from lxml import etree
from scripture.xpath import tripadvisor as ta

# Current Project
from . import api_v1

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36"  # noqa
}

logger = logging.getLogger("scripture.api.TripAdvisor")

comm_at_re = re.compile(r"([0-9 \-]+)")


def telephone(string):
    statement = []
    expr_re = re.compile(r"[a-z]+\+?='[0-9 \-]+'|document.write\(([a-z\+]+)\)")
    for line in string.split("\n"):
        match = expr_re.match(line)
        if not match:
            continue
        if match[1]:
            statement.append("tel = " + match[1])
            # statement.append(match[1])
        else:
            statement.append(match[0])
    expr = "\n".join(statement)
    if expr:
        g = {}
        exec(expr, g)
        try:
            return g["tel"].strip()
        except (KeyError, TypeError):
            logger.error("Bad telephone: %s", expr)
    else:
        return ""


def safe_xpath(tree, xp, name):
    try:
        fnd = tree.xpath("." + xp)
        return fnd[0]
    except IndexError:
        pass
        # logger.error("Not found %s" % name)


def published(tree):
    comment_at = safe_xpath(tree, "." + ta.comment_at, "published_at")
    if comment_at is not None:
        _at = comment_at.xpath("./@title")
        if _at:
            return _at[0]
        _at = comment_at.xpath("./text()")[0]
        try:
            match = comm_at_re.search(_at)
            return match[1]
        except (IndexError, TypeError):
            logger.error("at: %s, match: %s", _at, match.group())
            logger.error(etree.tostring(comment_at, encoding="unicode"))
    return ""


@api_v1.route("/comments/ta", methods=["GET", "OPTIONS"])
async def comments_from_tripadvisor(request):
    logger = logging.getLogger(__name__)
    url = request.args.get("url", None)
    if not url:
        data = {"status": 400, "error": "url of tripadvisor can not be empty"}
        logger.info(data)
        return json(data, status=400)
    if "cn.tripadvisor.com" not in url:
        url = url.replace("tripadvisor.com/", "tripadvisor.cn/")
    resp = requests.get(url, headers=headers)
    html = resp.content.decode('utf-8')
    status = resp.status_code
    # async with ClientSession() as session:
    #     async with session.get(url, headers=headers) as resp:
    #         html = unescape(await resp.text())
    #         status = resp.status

    if status != 200:
        data = {"status": status, "error": html}
        logger.warn(data)
        return json(data, status=status)

    comments_hash = []
    data = parser_commits(html, comments_hash)
    if len(data['comments']) >= 5:
        data.pop('max_pages')
        logger.info(f'url:{url} crawl ta comments success')
        return json(data)
    if 'max_pages' in data:
        max_pages = data.pop('max_pages')
    for i in range(max_pages):
        next_url = re.sub('-Reviews-', f'-Reviews-or{(i+1)*5}-', url)
        resp = requests.get(next_url, headers=headers)
        html = resp.content.decode('utf-8')
        status = resp.status_code
        # async with ClientSession() as session:
        #     async with session.get(next_url, headers=headers) as resp:
        #         html = unescape(await resp.text())
        #         status = resp.status

        if status != 200:
            logger.warning(f"error status_code with crawl {next_url}!comments : {data}")
            return json(data, status=status)
        data = parser_commits(html, comments_hash, data, max_pages)
        data.pop('max_pages')

        if len(data['comments']) >= 5:
            break
    logger.debug(f'comments_hash{comments_hash}')
    logger.info(f'url:{url} crawl ta comments success')
    return json(data)


def parser_commits(html, comments_hash=None, pre_data=None, pre_max_pages=None):
    parser = etree.HTML(html)
    data = pre_data or {"status": 200, "comments": []}
    max_pages = parser.xpath('//a[@data-page-number]//text()')
    if max_pages or pre_max_pages:
        data['max_pages'] = pre_max_pages or int(max_pages[-1])
    else:
        data['max_pages'] = 0
    data["cn_name"] = safe_xpath(parser, ta.cn_name, "cn_name")
    data["en_name"] = safe_xpath(parser, ta.en_name, "en_name")
    data["address"] = {
        "street": safe_xpath(parser, ta.address_street, "address.street"),
        "postal_code": safe_xpath(
            parser, ta.address_postalcode, "address.postal_code"
        ),
        "locality": safe_xpath(
            parser, ta.address_locality, "address.locality"
        ),
        "country": safe_xpath(parser, ta.address_country, "address.country"),
    }
    hotel_rating = safe_xpath(parser, '//div[@data-prwidget-name="common_bubble_rating"]/span/@class', "rating")
    if hotel_rating:
        data['rating'] = int(hotel_rating.split('_')[-1]) / 10
    else:
        data['rating'] = 'not find'
    tel_script = parser.xpath(ta.phone_script)
    tel = parser.xpath(ta.telephone)
    if tel_script:
        data["telephone"] = telephone(tel_script[0])
    elif tel:
        data["telephone"] = tel[0]
    else:
        data["telephone"] = ""
    data["average_rating"] = (
        safe_xpath(parser, ta.AVERAGE_RATING, "average_rating") or ""
    ).strip()
    listbox = parser.xpath(ta.comments_listbox)
    for box in listbox:
        try:
            _box = box.xpath(ta.comment_box1)[0]
            xpath_comment_by = ta.comment_user1 + ta.comment_by
        except IndexError:
            _box = box.xpath(ta.comment_box2)[0]
            xpath_comment_by = ta.comment_user2 + ta.comment_by
        to_translate = _box.xpath(ta.has_translate_button)
        if to_translate:
            locale = URL(to_translate[0]).query.get("sl")
        elif box.xpath(ta.has_translated_to):
            locale = "中文"
        else:
            locale = "中文"
        try:
            rating_element = _box.xpath(ta.rating_of_comment)
            if rating_element:
                rating = int(rating_element[0].split()[1].split("_")[1])
            else:
                logger.error(
                    "Failed to parse rating. %s",
                    etree.tounicode(_box, pretty_print=1),
                )
            if rating >= 10:
                rating /= 10

            if rating < 4:
                continue

        except (IndexError, TypeError) as e:
            rating = ""
            # x = box.xpath(ta.rating_box_of_comment)
            # if x:
            #     htm = etree.tostring(x, encoding="unicode")
            # else:
            #     htm = "None"
            # logger.error("Not found rating %s. url is %s", htm, url)

        title = safe_xpath(_box, ta.comment_title, "title")
        desc = safe_xpath(_box, ta.comment_desc, "description")

        # desc_hash = Simhash(desc).value
        # desc_hash = Simhash(desc).value
        # if desc_hash in comments_hash:
        #     continue
        # comments_hash.append(desc_hash)

        published_at = published(_box)

        published_by = safe_xpath(box, xpath_comment_by, "published_by")

        pictures = box.xpath('.' + ta.PICTURES)

        if not title or not desc or not rating:
            continue

        comments = {
            "title": title,
            "description": desc,
            "rating": str(rating),
            "published_at": published_at,
            "published_by": published_by,
            "locale": locale,
        }

        if pictures:
            comments['pictures'] = [{"image_url": img} for img in pictures]
        data["comments"].append(comments)
    return data
