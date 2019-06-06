# coding: utf8
"""Fetch google news"""

import logging
from datetime import datetime

import arrow
import gevent
import requests
import feedparser
from lxml import etree

from celery.utils.log import get_task_logger

from tasks import settings
from tasks.application import app
from tasks.utils.database import databases

logger = get_task_logger('tasks')   # pylint: disable=C0103


class Story(dict):
    """Model"""

    __db_table__ = None

    logger = logging.getLogger(__name__)

    @property
    def table(self):
        """get table"""
        return self.__db_table__

    @table.setter
    def table(self, collection):
        """set table"""
        self.__db_table__ = collection

    def save(self):
        """Save"""
        insert = self.copy()
        insert['created_at'] = datetime.now()
        update = {'updated_at': datetime.now()}

        if self.get('city'):
            update['city'] = insert.pop('city')
        if self.get('country_code'):
            update['country_code'] = insert.pop('country_code')
        if self.get('topic'):
            update['topic'] = insert.pop('topic')

        upsert_result = self.table.update_one(
            {'id': self.get('id')},
            {
                '$set': update,
                '$setOnInsert': insert
            },
            upsert=True
        )

        self.logger.info('Success to save story, %s', upsert_result.raw_result)
        if hasattr(upsert_result, 'inserted_id'):
            self['_id'] = upsert_result.inserted_id
            return self
        return self.table.find_one({'id': self['id']})


class AINews(Story):
    def save(self):
        return self.table.insert_one(self)

    @classmethod
    def from_story(cls, **kwargs):
        ai_news = cls()
        ai_news['scope'] = 'google'
        ai_news['category'] = kwargs.get('topic')
        ai_news['city'] = kwargs.get('city')
        ai_news['country'] = kwargs.get('country_code')
        ai_news['url'] = kwargs.get('link')
        ai_news['title'] = kwargs.get('title')
        ai_news['published_at'] = datetime.now()
        ai_news['published'] = True
        ai_news['capture_id'] = str(kwargs['_id'])
        if kwargs.get('summary'):
            summary = kwargs.get('summary')
            element = etree.HTML(summary)
            img_urls = element.xpath('//img/@src')
            if img_urls:
                ai_news['cover_image_url'] = img_urls[0]
            coverages = element.xpath('//a/@href')
            if coverages:
                ai_news['media_url'] = coverages[0]
            source = element.xpath('//font/text()')
            if source:
                ai_news['media_name'] = source[0]
        return ai_news


@app.task
def make_requests():
    """dispatch request by localtion or topic"""
    scripture = databases('scripture')

    avalible_topics = (
        'technology',
        'business',
        'entertainment',
        'sports',
        'science',
        'health'
    )
    for topic in avalible_topics:
        news_with_topic.apply_async([topic], time_limit=5, soft_time_limit=3)

        gevent.sleep(1)

    cursor = scripture.countries \
        .find({'population': {'$gte': 10000}}, no_cursor_timeout=True) \
        .sort('population', -1)
    for loc in cursor:
        location = '{}, {}'.format(loc['ascii_name'], loc['country_code'])
        news_with_loc.apply_async([location], time_limit=5, soft_time_limit=3)

        gevent.sleep(1)

    return True


@app.task
def news_with_loc(loc: str) -> bool:
    """fetch google news by location"""
    headers = {
        'User-Agent': ('Mozilla/5.0 (X11, Linux x86_64) AppleWebKit 537.36 '
                       '(KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36'),
    }
    session = requests.Session()
    session.proxies = settings.PROXIES
    resp = session.get(
        'https://news.google.com/news/rss/local/section/geo/{}'.format(loc),
        params={'ned': 'us', 'hl': 'en'},
        headers=headers,
        timeout=5,
    )
    if resp.status_code != 200:
        logger.warning(
            'Bad response %s %s %s',
            resp.status_code,
            resp.url,
            resp.reason
        )

    scripture = databases('scripture')
    hub = databases('ai')
    Story.__db_table__ = scripture.cp_stories
    AINews.__db_table__ = hub.ai_news
    feed = feedparser.parse(resp.text)
    for entry in feed['entries']:
        story = Story(entry)
        city, country_code = loc.rsplit(',', 1)
        story['city'] = city.strip()
        story['country_code'] = country_code.strip()
        published_at = arrow.get(
            story['published'],
            'D MMM YYYY HH:mm:ss ZZZ'
        )
        story['published_at'] = published_at.datetime
        story['scope'] = 'google'
        try:
            ai_story = AINews.from_story(**story.save())
            ai_story.save()
            logger.info('Successful to save %s to db', story['id'])
            logger.debug('Story %s', story)
        except Exception as exc:   # pylint: disable=W0703
            logger.error("%s", story)
            logger.exception(exc)
    return True


@app.task
def news_with_topic(topic: str) -> bool:
    """fetch google news by topic"""
    headers = {
        'User-Agent': ('Mozilla/5.0 (X11, Linux x86_64) AppleWebKit 537.36 '
                       '(KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36'),
    }
    session = requests.Session()
    session.proxies = settings.PROXIES
    url = 'https://news.google.com/news/rss/headlines/section/topic/' + \
        topic.upper()
    resp = session.get(
        url,
        params={'ned': 'us', 'hl': 'en'},
        headers=headers,
        timeout=5
    )
    if resp.status_code != 200:
        logger.warning(
            'Bad response %s %s %s',
            resp.status_code,
            resp.url,
            resp.reason
        )

    scripture = databases('scripture')
    hub = databases('ai')
    Story.__db_table__ = scripture.cp_stories
    AINews.__db_table__ = hub.ai_news

    feed = feedparser.parse(resp.text)
    for entry in feed['entries']:
        story = Story(entry)
        story['scope'] = 'google'
        story['topic'] = topic
        published_at = arrow.get(
            story['published'],
            'D MMM YYYY HH:mm:ss ZZZ'
        )
        story['published_at'] = published_at.datetime
        ai_story = AINews.from_story(**story)
        try:
            ai_story = AINews.from_story(**story.save())
            ai_story.save()
            logger.info('Successful to save %s to db', story)
        except Exception as exc:   # pylint: disable=W0703
            logger.exception(exc)
    return True
