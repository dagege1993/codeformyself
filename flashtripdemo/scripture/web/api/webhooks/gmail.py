# coding: utf8
"""Controllers for gmail
Created by songww
"""

import os
import logging

import json as jsonutil

from datetime import datetime
from urllib.parse import parse_qsl

from sanic import Blueprint
from sanic.response import json

from aioauth_client import GoogleClient
from aiohttp.web_exceptions import HTTPBadRequest

from web import settings
from web.utils.database import databases

from tasks import gmail  # pylint: disable=E0611

gmail_cb = Blueprint('gmail_callback', url_prefix='/webhooks/v1/gmail')  # noqa pylint: disable=C0103

logger = logging.getLogger(__name__)  # pylint: disable=C0103

if os.environ.get('AT_US', None):
    request_params = {}
else:
    request_params = dict(proxy=settings.HTTP_PROXY)  # noqa pylint: disable=C0103


class GMailClient(GoogleClient):
    """Gmail Client
    """
    name = 'gmail'
    base_url = 'https://www.googleapis.com/gmail/v1/'
    user_info_url = 'https://www.googleapis.com/oauth2/v2/userinfo'
    authorize_url = 'https://accounts.google.com/o/oauth2/auth'
    # access_token_url = 'https://accounts.google.com/o/oauth2/token'
    access_token_url = 'https://www.googleapis.com/oauth2/v4/token'

    @classmethod
    def user_parse(cls, data):
        """Parse information from provider."""
        yield 'id', data.get('sub') or data.get('id')
        yield 'username', data.get('nickname')
        yield 'first_name', data.get('given_name')
        yield 'last_name', data.get('family_name')
        yield 'locale', data.get('locale')
        yield 'link', data.get('link')
        yield 'picture', data.get('picture')
        yield 'email', data.get('email')

    async def refresh_access_token(
        self,
        refresh_token: str,
        grant_type: str = 'refresh_token',
        loop: str = None
    ):
        """Get an new access_token from OAuth provider by refresh_token.

        :returns: (access_token, provider_data)
        """

        if not isinstance(refresh_token, str):
            raise ValueError(
                f'refresh_token must be a string, but got '
                f'{type(refresh_token)}{refresh_token}'
            )  # noqa
        payload = {
            'refresh_token': refresh_token.strip('"').strip("'"),
            'grant_type': grant_type,
            'client_id': self.client_id,
            'client_secret': self.client_secret
        }

        response = await self.request(
            'POST', self.access_token_url, data=payload, loop=loop
        )

        if 'json' in response.headers.get('CONTENT-TYPE'):
            data = await response.json()

        else:
            data = await response.text()
            data = dict(parse_qsl(data))

        try:
            self.access_token = data['access_token']
        except Exception:
            raise HTTPBadRequest(reason=data)
        finally:
            response.close()

        return self.access_token, data


@gmail_cb.post('/<email>')
async def index(request, email):
    """Trigger parse gmail"""

    access_token = request.form.get('access_token')
    if not access_token:
        return json(
            {
                'status': 400,
                'error': 'access_token must be provided!'
            },
            status=400
        )
    refresh_token = request.form.get('refresh_token').strip('"').strip("'")
    if not refresh_token:
        return json(
            {
                'status': 400,
                'error': 'refresh_token must be provided!'
            },
            status=400
        )

    id_token = request.form.get('id_token')
    expires_in = int(request.form.get('expires_in', 3599))
    token_type = request.form.get('token_type')

    scripture = databases('scripture')

    scripture.g_users.update_one(
        {
            'email': email
        },
        {
            '$set': {
                'access_token': access_token,
                'refresh_token': refresh_token,
                # 'id_token': id_token,
                # 'expires_in': expires_in,
                # 'token_type': token_type,
                'email': email
            },
            '$currentDate': {
                'updated_at': True
            },
            '$setOnInsert': {
                'created_at': datetime.now()
            },
        },
        upsert=True
    )

    g = GMailClient(   # pylint: disable=C0103
        client_id=settings.GOOGLE_OAUTH_CLIENT_ID,
        client_secret=settings.GOOGLE_OAUTH_CLIENT_SECRET,
        access_token=access_token,
        request_params=request_params
    )

    _, data = await g.user_info()

    uri = f'users/{email}/messages'

    token = {
        'access_token': access_token,
        'refresh_token': refresh_token,
        'id_token': id_token,
        'expires_in': expires_in,
        'token_type': token_type
    }

    gmail.do_request.apply_async(
        (uri, token),
        link=gmail.dispatcher.s(email=email, uid=data['id'], token=token)
    )

    gmail.refresh_access_token.apply_async((email,), countdown=expires_in)

    return json(data)


@gmail_cb.get('/<email>')
async def orders(request, email):
    """List orders
    """
    SORT = {   # pylint: disable=C0103
        '-1': -1,
        '1': 1,
        'DESC': -1,
        'ASC': 1,
        'desc': -1,
        'asc': 1,
        -1: -1,
        1: 1
    }

    scripture = databases('scripture')

    query = {'email': email}

    u = await scripture.g_users.find_one({'email': email})  # noqa pylint: disable=C0103
    if not u:
        return json(
            {
                'error': 'User is not authenticated, please authenticate first',
                'status': 403
            },
            status=403
        )
    if not u.get('authenticated'):
        return json(
            {
                'error': 'User authenticate is expired!',
                'status': 401
            },
            status=401
        )

    sort = SORT.get(request.args.get('sort', 'DESC').upper())
    limit = int(request.args.get('limit', 20))
    page_number = int(request.args.get('page_number', 0))

    filters = request.args.get('filters')

    if filters:
        query['type'] = {'$in': filters}

    cursor = scripture.g_orders \
        .find(query) \
        .sort('created_at', sort) \
        .skip(limit * page_number) \
        .limit(limit)

    return json(
        jsonutil.dumps(
            [order async for order in cursor], ensure_ascii=False, default=str
        )
    )


@gmail_cb.patch('/<email>')
async def refresh_access_token(unused_request, email):
    """Refresh access token"""

    scripture = databases('scripture')

    u = await scripture.g_users.find_one({'email': email})  # noqa pylint: disable=C0103

    g = GMailClient(   # pylint: disable=C0103
        client_id=settings.GOOGLE_OAUTH_CLIENT_ID,
        client_secret=settings.GOOGLE_OAUTH_CLIENT_SECRET,
        access_token=u['access_token'],
        request_params=request_params
    )

    try:
        _, data = await g.refresh_access_token(u['refresh_token'])

        unused_user, u_info = await g.user_info()

        data.update(u_info)
        data['authenticated'] = True

        await scripture.g_users.update_one(
            {
                'email': email
            }, {
                '$set': data,
                '$currentDate': {
                    'updated_at': True,
                    'token_refreshed_at': True
                }
            }
        )
    except Exception as e:  # pylint: disable=W0703,C0103
        logger.exception(e)
        await scripture.g_users.update_one(
            {
                'email': email
            }, {
                '$set': {
                    'authenticated': False
                },
                '$currentDate': {
                    'updated_at': True,
                    'token_refreshed_at': True
                }
            }
        )
        return json({'text': False}, status=401)

    return json(data)
