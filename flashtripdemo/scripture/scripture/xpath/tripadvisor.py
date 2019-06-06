# coding: utf8

comments_listbox = (
    '//div[@class="review-container"]'
    '//div[@class="rev_wrap ui_columns is-multiline "]'
)

comment_box1 = './/div[@class="ui_column is-9"]'
comment_box2 = './/div[@class="col2of2"]'

comment_user1 = '//div[@class="ui_column is-2"]'
comment_user2 = '//div[@class="col1of2"]'

comment_title = (
    '//div[contains(@class,"quote")]/a/span[@class="noQuotes"]/text()'
)

comment_desc = '//div[@class="entry"]/p/text()'

rating_of_comment = './/span[contains(@class,"ui_bubble_rating")]/@class'

comment_at = '//span[contains(@class, "ratingDate")]'

has_translate_button = '//div[@class="wrap"]'
has_translate_button += '/div/span[contains(@class, "ui_button")]/@data-url'

comment_by = (
    '//div[@class="memberOverlayLink clickable"]/div[@class="info_text"]/div/text()'
)

has_translated_to = '//div[@class="headers"]//span[text()="译"]/@class'
has_translated_from = '//div[@class="headers"]//a/text()'
detail_in_origin_language = '//div[@class="headers"]//a/@href'

cn_name = '//h1[@id="HEADING"]/text()'
en_name = '//h1[@id="HEADING"]/div/text()'

address_street = '//span[@class="detail"]/span[@class="street-address"]/text()'
address_postalcode = (
    '//span[@class="detail"]/span[@class="postal-code"]/text()'
)
address_locality = '//span[@class="detail"]/span[@class="locality"]/text()'
address_country = '//div[@class="where_with_highlight"]/input/@value'

phone_script = '//div[contains(@class, "phone")]/span/script/text()'
telephone = '//span[@class="is-hidden-mobile detail"]/text()'

AVERAGE_RATING = (
    '//div[@class="react-container"]//div[@class="ui_columns is-multiline"]'
    '//span[@class="overallRating"]/text()'
)

PICTURES = '//span[@class="imgWrap "]//img[@class="centeredImg noscript"]/@src'