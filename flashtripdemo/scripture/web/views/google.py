# coding: utf8
"""Google Mail"""

import os
import logging

from urllib.parse import parse_qsl
from datetime import datetime, timedelta

import jwt

from aioauth_client import GoogleClient

from sanic import Blueprint
from sanic.response import json, redirect, html
from aiohttp.web_exceptions import HTTPBadRequest

from web.utils.database import databases
from tasks import gmail as gmail_tasks

google_bp = Blueprint('google', url_prefix='/views/google')  # noqa pylint: disable=C0103
google_auth_bp = Blueprint('auth.google', url_prefix='/views/auth/google')  # noqa pylint: disable=C0103

GOOGLE_OAUTH_CLIENT_ID = (
    '543145811859-ebhl03of57rchnolmdpuphqinqf1mavn.apps.'
    'googleusercontent.com'
)
GOOGLE_OAUTH_CLIENT_SECRET = 'sgPYw2fH7efvLoDHKgfC1Q2a'

logger = logging.getLogger(__name__)  # noqa pylint: disable=C0103

if os.environ.get('AT_US', None):
    request_params = {}
else:
    from web import settings
    request_params = dict(proxy=settings.HTTP_PROXY)  # noqa pylint: disable=C0103


class GMailClient(GoogleClient):
    """Gmail"""
    base_url = 'https://www.googleapis.com/gmail/v1/'
    name = 'gmail'
    user_info_url = 'https://www.googleapis.com/oauth2/v2/userinfo'
    _request_params = {}

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
        self, refresh_token, grant_type='refresh_token', loop=None
    ):
        """Get an new access_token from OAuth provider by refresh_token.

        :returns: (access_token, provider_data)
        """

        if not isinstance(refresh_token, str):
            raise ValueError(
                'refresh_token must be a string, but got '
                f'{type(refresh_token)}{refresh_token}'  # noqa
            )
        payload = {
            'refresh_token': refresh_token,
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
            raise HTTPBadRequest(reason='Failed to update OAuth access token.')
        finally:
            await response.release()

        return self.access_token, data


def auth_required(fn):  # pylint: disable=C0103
    """func doc"""

    async def wrapper(request, **kwargs):
        """func doc"""

        user_id = kwargs.get('user_id')
        logger.info(
            'Request %s?%s with body %s', request.url, request.args,
            request.body
        )
        user_info = await databases('scripture').g_users.find_one(
            {
                '$or': [{
                    'email': user_id
                }, {
                    'id': user_id
                }],
            }
        )
        # request['user_id') = user_id
        if not user_info:
            logger.info('User info of %s is empty', user_id)
            logger.info('Callback for auth redirect is %s', request.url)
            return redirect(
                '/views/auth/google?callback={}'.format(request.url)
            )
        g = GMailClient(   # pylint: disable=C0103
            client_id=GOOGLE_OAUTH_CLIENT_ID,
            client_secret=GOOGLE_OAUTH_CLIENT_SECRET,
            base_url='https://www.googleapis.com/gmail/v1/',
            access_token=user_info['access_token'],
            user_info_url='https://www.googleapis.com/oauth2/v2/userinfo',
            request_params=request_params
        )

        exp = timedelta(seconds=user_info['expires_in']) + \
            user_info['updated_at']
        logger.info('Logined as %s, %s', user_id, user_info)
        logger.info('now is %s, exp is: %s', datetime.now(), exp)
        if datetime.now() >= exp:
            r_token = user_info.get('refresh_token')
            if not r_token:
                return redirect(
                    '/views/auth/google?callback={}'.format(request.url)
                )
            token, data = await g.refresh_access_token(r_token)
            data['updated_at'] = datetime.now()
            data['email'] = user_id
            await databases('scripture').g_users.update_one(
                {
                    '$or': [{
                        'email': user_id
                    }, {
                        'id': user_id
                    }]
                },
                {'$set': data,
                 '$setOnInsert': {
                     'created_at': datetime.now()
                 }},
                upsert=True
            )

            logger.info('Success to update access token of user %s', user_id)
            g.access_token = token

        if 'last_name' not in user_info:
            try:
                user, info = await g.user_info()
            except HTTPBadRequest as exc:
                logger.exception(exc)
                return redirect(
                    '/views/auth/google?callback={}'.format(request.url)
                )

            logger.info('User %s, info %s', user.__dict__, info)
            u = user.__dict__.copy()  # pylint: disable=C0103
            u['updated_at'] = datetime.now()
            await databases('scripture').g_users.update_one(
                {
                    '$or': [{
                        'email': user_id
                    }, {
                        'id': user_id
                    }]
                }, {'$set': u,
                    '$setOnInsert': {
                        'created_at': datetime.now()
                    }},
                upsert=True
            )

        request['g'] = g

        return await fn(request, **kwargs)

    return wrapper


@google_auth_bp.get('/')
async def auth(request):
    """Auth"""
    request_host = f"{request.scheme}://{request.host}"
    g = GMailClient(    # pylint: disable=C0103
        client_id=GOOGLE_OAUTH_CLIENT_ID,
        client_secret=GOOGLE_OAUTH_CLIENT_SECRET,
        base_url='https://www.googleapis.com/gmail/v1/',
        request_params=request_params
    )

    before = request.args.get('callback')
    if before:
        if 'set_cookies' in request:
            request['set_cookies'].append(('callback', before))
        else:
            request['set_cookies'] = [('callback', before)]

    scopes = ' '.join(
        [
            'https://www.googleapis.com/auth/userinfo.email',
            'https://www.googleapis.com/auth/userinfo.profile',
            'https://www.googleapis.com/auth/gmail.readonly',
        ]
    )

    code = request.args.get('code')

    if not code:
        response = redirect(
            g.get_authorize_url(
                scope=scopes,
                redirect_uri=f'{request_host}/views/auth/google',
                access_type='offline'
            )
        )
        for cookie_name, value, *_ in request.get('set_cookies', []):
            if value is not None:
                response.cookies[cookie_name] = value
            else:
                del response.cookies[cookie_name]

        return response

    try:
        token, data = await g.get_access_token(
            code, redirect_uri=f'{request_host}/views/auth/google'
        )
    except HTTPBadRequest as exc:
        print('-----------------------------------')
        print(exc)
        response = redirect('/views/auth/google')
        for cookie_name, value, *_ in request.get('set_cookies', []):
            if value is not None:
                response.cookies[cookie_name] = value
            else:
                del response.cookies[cookie_name]

        return response

    try:
        jwt_code = jwt.decode(data['id_token'], 'secret', verify=False)
        email = jwt_code.get('email')
        verified = jwt_code.get('email_verified')
        logger.info(verified)
    except ValueError:
        logger.error(data['id_token'])

    logger.debug(
        'Success to update access_token %s from google for user %s', token,
        email
    )

    data['updated_at'] = datetime.now()

    data['email'] = email

    update_result = await databases('scripture').g_users.update_one(
        {
            '$or': [{
                'email': email
            }, {
                'id': email
            }]
        },
        {'$set': data},
        upsert=True,
    )

    if update_result.modified_count == 0:
        logger.warning('Failed to update access_token in db, %s', email)

    before = request.cookies.get('callback')

    response = redirect(before)
    response.cookies['user_email'] = email
    del response.cookies['callback']
    return response


@google_bp.get('/mails/<user_id>')
@auth_required
async def emails(request, user_id):
    """List emails"""

    request_host = f"{request.scheme}://{request.host}"

    fmt = request.args.get('format', 'html')

    orders = databases('scripture').g_orders \
        .find({
            '$or': [{
                'id': user_id
            }, {
                'email': user_id
            }]
        })

    # g = request['g']   # pylint: disable=C0103

    #   user_id = request['user'].id

    # d = await g.request(   # pylint: disable=C0103
    #     'get', 'users/{user_id}/messages'.format(user_id=user_id)
    # )

    # jsn = await d.json()

    # async def fetch_message(msg_id):
    #     """Fetch message
    #     """
    #     resp = await g.request(
    #         'get',
    #         f'users/{user_id}/messages/{msg_id}',  # noqa
    #     )
    #     msg_text = await resp.text()
    #     try:
    #         msg = jsontool.loads(msg_text.strip())
    #         for header in msg['payload']['headers']:
    #             if header['name'].lower() != 'subject':
    #                 continue
    #             value = header['value'].lower().strip()
    #             if ('confirm' in value or 'itinerary' in value or
    #                     'reservation' in value or
    #                     'Your Flight Receipt' in value):  # noqa
    #                 logger.info(header)
    #                 subject = header['value']
    #                 break
    #         else:
    #             return None
    #         _html = []
    #         if msg['payload']['mimeType'].startswith('multipart'):
    #             for part in msg['payload']['parts']:
    #                 if part['body']['size'] == 0:
    #                     for subpart in part['parts']:
    #                         if 'data' not in subpart['body']:
    #                             continue
    #                         subpart['body']['data'] = base64 \
    #                             .urlsafe_b64decode(subpart['body']['data']) \
    #                             .strip()
    #                         _html.append(subpart['body']['data'])
    #                 elif 'data' in part['body']:
    #                     part['body']['data'] = base64.urlsafe_b64decode(
    #                         part['body']['data']
    #                     ) \
    #                         .strip()
    #                     _html.append(part['body']['data'])
    #         elif 'data' in msg['payload']['body']:
    #             msg['payload']['body']['data'] = base64 \
    #                 .urlsafe_b64decode(msg['payload']['body']['data']) \
    #                 .strip()
    #             _html.append(msg['payload']['body']['data'])
    #         else:
    #             logger.warning('unknown type of mail content %s', msg)
    #         await databases('scripture').gmail.update_one(
    #             {
    #                 'msg_id': msg_id,
    #                 'user_id': user_id
    #             }, {
    #                 '$set': {
    #                     'msg_id': msg_id,
    #                     'html': _html,
    #                     'json': msg,
    #                     'user_id': user_id
    #                 }
    #             },
    #             upsert=True
    #         )
    #         return {'id': msg_id, 'subject': subject}
    #     except Exception as exc:  # noqa pylint: disable=W0703
    #         logger.exception(exc)
    #         return None

    # coros = []
    # for message in jsn['messages']:
    #     coros.append(fetch_message(message['id']))
    # messages = await asyncio.gather(*coros)
    # content = []
    # json_content = []
    # for message in messages:
    #     if message:
    #         content.append(
    #             f'<a href="{request_host}/views/google/mail/{message["id"]}'
    #             f'/{user_id}">{message["subject"]}</a>'  # noqa
    #         )
    #         jsn_find = await databases('scripture').gmail.find_one(
    #             {
    #                 'msg_id': message['id'],
    #                 'user_id': user_id,
    #                 'json': {
    #                     '$exists': 1
    #                 },
    #             }
    #         )

    #         if jsn_find:
    #             json_content.append(jsn_find['json'])
    #         else:
    #             logger.error(
    #                 'Not json found msg_id: %s, user_id: %s', message['id'],
    #                 user_id
    #             )

    user_info = await databases('scripture').g_users.find_one(
        {
            '$or': [{
                'email': user_id
            }, {
                'id': user_id
            }],
        }
    )
    user_info['_id'] = str(user_info['_id'])

    gmail_tasks.do_request.apply_async(
        (f'users/{user_info["email"]}/messages', user_info),
        link=gmail_tasks.dispatcher.s(
            email=user_info['email'], uid=user_info['id'], token=user_info
        )
    )

    if await orders.count() < 0:
        return json({'err_msg': 'Not found'}, 404)

    if fmt == 'json':
        _orders = []
        async for order in orders:
            order['_id'] = str(order['_id'])
            _orders.append(order)
        return json({'status': 200, 'orders': _orders})

    links = []

    async for order in orders:
        if 'subject' not in order:
            continue
        links.append(
            f'<a href="{request_host}/views/google/mail/'
            f'{order["message_id"]}/{user_info["id"]}">'
            f'{order["subject"]}</a>'
        )

    return html("<li>".join(links))


@google_bp.get('/mail/<msg_id>/<user_id>')
async def mail_content(request, msg_id, user_id):  # pylint: disable=W0613
    """Get content"""
    record = await databases('scripture') \
        .g_mails \
        .find_one({
            'msg_id': msg_id,
            '$or': [
                {
                    'email': user_id
                }, {
                    'id': user_id
                }
            ]
        })
    return html(b'\n'.join(record['html']).decode('utf8').strip())
