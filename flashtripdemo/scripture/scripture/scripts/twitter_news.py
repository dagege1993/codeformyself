# coding: utf8

try:
    import ujson as json
except ImportError:
    import json

import uvloop
import asyncio
import logging
from yarl import URL
from aiohttp import ClientSession
from datetime import datetime
from lxml.etree import HTML
from aioauth_client import TwitterClient
from motor.motor_asyncio import AsyncIOMotorClient as MongoClient

from scripture import settings

logging.basicConfig(
    format='%(asctime)s %(name)s %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger('twitter.news')

url = 'https://userstream.twitter.com/1.1/user.json'

proxy = 'http://172.17.1.198:1118'

tweet = TwitterClient(
    consumer_key='buAFwd0vZPgRkk92GdNkqWobf',
    consumer_secret='LNvjEUQzFqKszTeh5jnz2otZrEowZ06ShN1FOWmJ79TPpEYX1j',
    oauth_token='879182607505793024-UhuTlH1bABSVw5TpR1ejiA1PsFJQsAn',
    oauth_token_secret='suWywcV5ezZwSiCXTZm2xwIYW1xz7SQcuyTnhqGO7x3xo',
    base_url='https://userstream.twitter.com/1.1/',
    request_params={'proxy': proxy}
)

mc = MongoClient(settings.MONGO)


async def parse_location(tree):
    tree = HTML(html)
    tree.xpath()
    return None


async def parse_tags(html):
    pass


class BaseModel:

    connection = None
    database_name = None
    collection_name = None

    @classmethod
    def set_connection(cls, connection):
        cls.connection = connection
        cls.database_name = connection.get_default_database().name
        cls.collection_name = cls.collection_name \
            or cls.to_snake_case(cls.__name__)
        return cls

    @classmethod
    def to_snake_case(cls, camel_case):
        return (
            ''.join([
                "_" + x.lower()
                if i < len(camel_case) - 1 and x.isupper() and out[i + 1].islower()  # noqa
                else x.lower() + "_"
                if i < len(camel_case) - 1 and x.islower() and out[i + 1].isupper()  # noqa
                else x.lower() for i, x in enumerate(list(camel_case))])
        ) \
            .lstrip('_') \
            .replace('__', '_')

    def __getattr__(self, attr):
        try:
            self[attr]
        except KeyError:
            raise AttributeError(f'Model object has no attribute {attr}')  # noqa

    def __setattr__(self, attr, value):
        self[attr] = value
        return value

    async def find_one(**args):
        return self.connection.find_one()


def Base(connection):
    BaseModel.set_connection(connection)
    return BaseModel


Model = BaseModel(mc)


class TweetNews(Model):
    database_name = 'scripture'
    collection_name = 'twitter_news'


class BBC:

    def __init__(self, tweet_id, url):
        self.news_src = URL(url)
        self.tweet_id = tweet_id
        self.tags = []

    def news_tags(self, tree):
        tags = []
        first_tag = tree.xpath(
            '//span[@id="comp-index-title"]/span/a/text()'
        )
        if first_tag:
            tags.append(first_tag[0])
        xp = '//div[@id="site-container"]/div[contains(@class, "site-brand")]'
        xp += '/div[contains(@class, "secondary-navigation")]/nav/ul/li/a/span'
        xp += '/text()'
        other_tags = tree.xpath(xp)
        tags.extend(other_tags)
        return tags

    def sport_tags(self):
        self.tags = []

    def _location(self):
        self.location = ''

    async def parse(self):
        async with ClientSession() as request:
            async with request.get(url, proxy=proxy) as resp:
                html = await resp.text()

        tree = HTML(html)

        if self.news_tags.path.startswith('/sport/live'):
            self.tags = ['sport', 'live']
        elif self.news_tags.path.startswith('/news'):
            self.tags = self.news_tags(tree)
        else:
            pass

        self._location()

    def save(self):
        pass


async def parse_news(url, type):
    tree = HTML(html)


async def main():

    stream = await tweet.request('get', 'user.json')

    async for line in stream.content:
        line = line.strip()
        if line == b'':
            print('empty line')
            continue
        n = json.loads(line)
        if 'friends' in n:
            logger.debug(n)
            continue

        print(n)
        continue

        now = datetime.now()

        if 'delete' in n:
            dlt = await mc.scripture.twitter_news.update_one(
                {'id': n['status']['id'], 'user.id': n['status']['user_id']},  # noqa
                {'deleted_at': now}
            )
            logger.info(f'To mark {n["id"]} as deleted {dlt.modified_count}')  # noqa
        else:
            n['inserted_at'] = now
            ist = await mc.scripture.twitter_news.insert_one(n)
            logger.info('Added %s', ist.inserted_id)


if __name__ == '__main__':
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
