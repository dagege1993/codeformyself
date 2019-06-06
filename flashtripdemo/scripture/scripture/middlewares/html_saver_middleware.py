# coding: utf8
"""Created by songww
"""

import lzma
import logging

import oss2
from yarl import URL
oss2.defaults.logger = logging.getLogger('oss')    # patch oss logger


class HtmlSaverMiddleware(object):
    """Middleware for save html to oss
    """

    logger = logging.getLogger(__name__)

    def __init__(self, settings):
        self.settings = settings

        endpoint = settings.get('OSS_SCRIPTURE_ENDPOINT')
        auth = oss2.Auth(
            settings.get('OSS_SCRIPTURE_ACCESS_KEY_ID'),
            settings.get('OSS_SCRIPTURE_ACCESS_KEY_SECRET')
        )
        bucket = settings.get('OSS_SCRIPTURE_BUCKET')
        self.oss = oss2.Bucket(auth, endpoint, bucket)

    @classmethod
    def from_crawler(cls, crawler):
        """Override
        Args:
        Returns:
        """
        middleware = cls(crawler.settings)
        return middleware

    def process_response(self, request, response, spider):
        """Override
        Args:
        Returns:
        """
        if response.status > 299:
            return response
        url = response.url.endswith('/') and response.url[:-1] or response.url  # pylint: disable=R1706
        url = URL(url)
        query = url.query
        if not query:
            self._save_compressed(url, response.body)
            return response
        check_in = query.get('q-check-in')
        hcom_id = query.get('hotel-id')
        if not check_in and not hcom_id and url.path.startswith('/ho'):
            url = url.with_query({})
        else:
            url = url.join(URL(f'/ho{hcom_id}/{check_in}'))  # noqa
        self._save_compressed(url, response.body)
        return response

    def _save_compressed(self, url, body):
        """LZMA only handle bytes object
        And add postfix .xz for filename
        """
        if isinstance(body, str):
            body = body.encode('utf8')
        fname = str(url.with_scheme('').with_query({}))[2:]
        fname = f'{fname}.xz'
        self.oss.put_object(fname, lzma.compress(body))
