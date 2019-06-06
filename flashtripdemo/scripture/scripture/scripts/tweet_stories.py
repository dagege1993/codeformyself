# coding: utf8
"""Created by songww
"""

import asyncio
import logging
import time

from hashlib import sha1
from datetime import datetime
from random import SystemRandom
from urllib.parse import urlsplit

import ujson
import uvloop

from aiohttp import ClientSession
from aiohttp.client import _SessionRequestContextManager
from aioauth_client import TwitterClient

from mmongo.document import Document
from mmongo.fields import BoolField, EnumField, StringField

from motor.motor_asyncio import AsyncIOMotorClient as MotorClient

from scripture import settings

random = SystemRandom().random  # pylint: disable=C0103
logging.basicConfig(
    level=logging.DEBUG,
    format='[%(asctime)s] %(levelname)s - %(name)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M%S'
)


class DatetimeField(StringField):
    _types = (datetime,)

    def ensure_value(self, value):
        if not value:
            if callable(self.default):
                return self.default()
            return self.default
        return value


class TwitterStream(TwitterClient):
    async def request(self, method, url, params=None, headers=None, timeout=10,
                      loop=None, **aio_kwargs):
        """Make a request to provider."""
        oparams = {
            'oauth_consumer_key': self.consumer_key,
            'oauth_nonce': sha1(str(random()).encode('ascii')).hexdigest(),
            'oauth_signature_method': self.signature.name,
            'oauth_timestamp': str(int(time.time())),
            'oauth_version': self.version,
        }
        oparams.update(params or {})

        request_params = self.request_params.copy()
        request_params.update(aio_kwargs)

        if self.oauth_token:
            oparams['oauth_token'] = self.oauth_token

        url = self._get_url(url)

        if urlsplit(url).query:
            raise ValueError('Request parameters should be in the "params"'
                             'parameter, not inlined in the URL')

        oparams['oauth_signature'] = self.signature.sign(
            self.consumer_secret, method, url,
            oauth_token_secret=self.oauth_token_secret, **oparams)
        self.logger.debug("%s %s", url, oparams)
        session = ClientSession(conn_timeout=0, read_timeout=0)
        return _SessionRequestContextManager(
            session._request(method, url, params=oparams, headers=headers,
                             **request_params),
            session
        )


class AINews(Document):
    """ai_news"""
    __collection_name__ = 'ai_news'
    scope = EnumField(('google', 'twitter'), required=True)
    city = StringField(required=False)
    country = StringField(required=False)
    places = StringField(required=False)
    category = StringField(required=False)
    url = StringField(required=False)
    title = StringField(required=False)
    cover_image_url = StringField(required=False)
    media_name = StringField()
    media_url = StringField()
    media_avatar = StringField()
    user_name = StringField()
    user_avatar = StringField()
    published_at = DatetimeField(required=True)
    published = BoolField(required=True, default=True)
    capture_id = StringField(required=True)


class Story(Document):
    """cp_stories"""
    __collection_name__ = 'cp_stories'
    scope = EnumField(('google', 'twitter'), required=True)
    inserted_at = DatetimeField(required=True, default=datetime.now)
    updated_at = DatetimeField(required=True, default=datetime.now)


async def main(loop, queue):
    auth = {
        'consumer_key': 'buAFwd0vZPgRkk92GdNkqWobf',
        'consumer_secret': 'LNvjEUQzFqKszTeh5jnz2otZrEowZ06ShN1FOWmJ79TPpEYX1j',
        'oauth_token': '879182607505793024-UhuTlH1bABSVw5TpR1ejiA1PsFJQsAn',
        'oauth_token_secret': 'suWywcV5ezZwSiCXTZm2xwIYW1xz7SQcuyTnhqGO7x3xo'
    }

    # proxy = 'http://172.17.1.198:1118'

    logger = logging.getLogger('tweet-news')

    tweet = TwitterStream(
        **auth,
        timeout=0,
        request_params={'timeout': 0},
        base_url='https://userstream.twitter.com/1.1/'
    )

    # async with ClientSession() as session:
    #     async with session.get(tweet_endpoint) as stream:
    #         async for line in stream.content:
    #             line = line.strip()
    #             if line == b'':
    #                 logger.debug('Empty line!')
    #                 continue
    #             message = ujson.loads(line.decode('utf8'))
    #             if 'friends' in message:
    #                 logger.info('Friends: %s', message)
    #                 continue

    #             now = datetime.now()

    #             if 'delete' in message:
    #                 story = Story({
    #                     'id': message['id'],
    #                     'user': {
    #                         'id': message['status']['user_id']
    #                     }
    #                 })
    #                 story.update_one({'deleted_at': now})
    #                 logger.info('Mark as deleted: %s', story._id)
    #                 continue
    #             story = Story(message)
    #             story.save()
    #             logger.info('New story saved: %s', story._id)
    resp = await tweet.request('get', 'user.json')
    async with resp as stream:
        # async for line in stream.content:
        while True:
            line = await stream.content.readline()
            line = line.strip()
            if line == b'':
                logger.debug('Empty line!')
                continue
            message = ujson.loads(line.decode('utf8'))
            if 'friends' in message:
                logger.info('Friends: %s', message)
                continue

            message['scope'] = 'twitter'
            await queue.put(message)


async def process(loop, queue):

    AINews.set_connection(MotorClient(settings.AI_MONGO, io_loop=loop), loop)
    # AINews.set_connection(MotorClient(settings.MONGO, io_loop=loop), loop)
    Story.set_connection(MotorClient(settings.MONGO, io_loop=loop), loop)

    logger = logging.getLogger('tweet-news.process')

    while True:

        message = await queue.get()
        if not message:
            continue

        now = datetime.now()

        if 'delete' in message:
            story = Story({
                'id': message['id'],
                'user': {
                    'id': message['status']['user_id']
                },
                'scope': 'twitter'
            })
            story.update_one({'deleted_at': now})
            logger.info('Mark as deleted: %s', story['_id'])
            continue
        message['scope'] = 'twitter'
        story = Story(**message)
        await story.save()
        logger.info('New story saved: %s', story['_id'])
        entities = story.get('extended_tweet', story).get('entities')
        user = story.user
        try:
            url = entities.get('urls')[0].get('expanded_url')
            cover_image_url = entities.get('media')[0].get('media_url_https')
        except Exception as exc:
            logger.exception(exc)
            logger.error('Bad message %s', message)
            continue
        ai_story = AINews({
            'scope': 'twitter',
            'category': '',
            'url': url,
            'title': story.text,
            'cover_image_url': cover_image_url,
            'media_name': user['screen_name'],
            'media_url': user['url'],
            'media_avatar': user['profile_image_url_https'],
            'user_name': user['name'],
            # 'user_avatar': ,
            'published_at': now,
            'published': True,
            'capture_id': str(story['_id'])
        })
        await ai_story.save()
        logger.info('New ai_news saved: %s', ai_story['_id'])


if __name__ == '__main__':
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    loop = asyncio.get_event_loop()   # pylint: disable=C0103
    message_q = asyncio.Queue()   # pylint: disable=C0103
    loop.run_until_complete(
        asyncio.gather(
            main(loop, message_q),
            process(loop, message_q)
        )
    )
