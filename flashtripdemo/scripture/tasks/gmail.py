# coding: utf8
"""Tasks for parse GMail
Created by songww
"""

from typing import Dict, Any
from datetime import datetime, timedelta

import requests

from celery import group
from celery.utils.log import get_task_logger
from celery.exceptions import Ignore

from tasks import settings
from tasks.application import app
from tasks.utils.session import session
from tasks.utils.database import databases
from tasks.errors.parse_error import ParseError, ParserNotFound
from tasks.parsers import Parser

logger = get_task_logger('tasks')  # pylint: disable=C0103

mapping = {
    'hotel': 'hotel_orders',
    'flight': 'flight_orders',
    'restaurant': 'restaurant_orders'
}
ai_base = 'https://ai.weego.me/api/v3/ai/user_profiles/'


@app.task
def refresh_access_token(email: str):  # Type: Bool
    """Refresh access token by refresh token
    """
    # scripture = databases('scripture')
    # user = scripture.g_users.find_one({'email': email})

    resp = requests.patch(
        'http://scripture.weegotr.com/webhooks/v1/gmail/' + email
    )

    if resp.status_code == 200:
        logger.info('Successed to refresh access_token for %s', email)

        countdown = resp.json()['expires_in']

        refresh_access_token.apply_async((email,), countdown=countdown)

        return True

    logger.error(
        'Failed to refresh access_token of %s, caused by %s', email, resp.text
    )
    return False


@app.task
def do_request(
    uri: str, token: Dict[str, Any], params: Dict = None, method: str = 'get'
):  # Type: Bool
    """Request to gmail
    Args:
        uri: string
        token: dict
        params: dict
        method: string
    Returns:
        None
    Raises:
        Ingore
    """

    base_url = 'https://www.googleapis.com/gmail/v1/'

    if not isinstance(uri, (str, bytes)):
        logger.error(
            'Bad request uri<%s> token<%s> params<%s> http_method<%s>', uri,
            token, params, method
        )
        raise Exception()

    url = base_url + uri

    if params is None:
        params = {}

    _session = session(token)

    resp = _session.request(
        method,
        url,
        params=params,
        client_id=settings.GOOGLE_CLIENT_ID,
        client_secret=settings.GOOGLE_CLIENT_SECRET
    )
    if resp.status_code == 200:
        logger.debug(
            'Success to request %s, %s', url, token['access_token'][:20]
        )
        return resp.json()
    logger.error(
        'Failed to request %s, status_code %s, respone %s', url,
        resp.status_code, resp.text
    )
    raise Ignore(None)


@app.task
def dispatcher(messages: Dict[str, Any], email: str, uid: str, token: str):
    """Dispatch request and response
    Args:
        messages: List
        email: string
        token: sting
    Returns:
        None
    Raises:
        Ignore
    """

    if len(messages['messages']) < 1:
        raise Ignore(None)

    save_cb = save_order_message.s(email=email)
    parse_order_message_cb = parse_order_message.s(email=email, uid=uid)
    parse_order_message_cb.link(save_cb)
    is_order_message_cb = is_order_message.s()
    is_order_message_cb.link(parse_order_message_cb)
    # do_request_s = do_request.s(token=token)
    group([
        do_request.signature(
            (f'users/{email}/messages/{message["id"]}', token),
            link=is_order_message_cb
        )
        for message in messages['messages'][:-1]
    ]) \
        .apply_async()
    last_message = messages['messages'][-1]
    result = do_request(
        f'users/{email}/messages/{last_message["id"]}', token=token
    )

    scripture = databases('scripture')

    last_fetched_at = scripture.g_users \
        .find_one({'email': email}) \
        .get('last_fetched_at')

    if must_request_next_page(result, last_fetched_at):
        params = {'pageToken': messages['nextPageToken']}
        do_request.apply_async(
            (f'users/{email}/messages/', token, params),
            link=dispatcher.s(email=email, uid=uid, token=token)
        )
    else:
        incremental_fetch.apply_async(
            (email,), eta=datetime.now() + timedelta(days=1)
        )

    is_order_message.apply_async((result,), link=parse_order_message_cb)


def must_request_next_page(
    message: Dict, last_fetched_at: datetime = None
) -> bool:
    """Continue request next page"""
    now = datetime.now()
    delta = last_fetched_at and (now - last_fetched_at).days or 31
    for header in message['payload']['headers']:
        if header['name'] == 'X-Received':
            received_time = header['value'].split(',')[-1].split('(')[0].strip()
            received_time = '-'.join(received_time.split(' ')[:3])
            received_time = datetime.strptime(received_time, '%d-%b-%Y')
            if (now - received_time).days < delta:
                return True

    raise Ignore(None)


@app.task
def is_order_message(message: Dict[str, Any]) -> Dict[str, Any]:
    """If is message of order
    Args:
        param message: dict
    Returns:
        Bool
    Raises:
        Ignore
    """
    if not isinstance(message, dict):
        logger.warning('%s, %s', type(message), message)
        raise Ignore(None)
    if 'payload' not in message or 'headers' not in message['payload']:
        logger.warning(message)
        raise Ignore(None)
    for header in message['payload']['headers']:
        if header['name'] == 'Subject':
            subject = header['value'].lower()
            break
    else:
        raise Ignore(None)

    if 'booking' or 'reservation' in subject:
        return message
    raise Ignore(None)


@app.task
def parse_order_message(message: Dict, email: str, uid: str) -> Dict:
    """Choice parser to parse message
    """
    if not message:
        raise Ignore(None)

    try:
        parser = Parser(message, email, uid)
    except ParserNotFound as notfound:
        logger.warn(notfound)
        raise Ignore(None)
    except TypeError:
        logger.exception('message[%s], email[%s]', message['id'], email)
        raise Ignore(None)

    try:
        return parser.parse()
    except ParseError as exc:
        logger.exception(exc)
        raise Ignore(None)


@app.task
def save_order_message(order_message: Dict, email: str) -> Dict[str, Any]:
    """Save parsed message to mongo
    """
    if not order_message or \
            not isinstance(order_message, dict) or \
            'message_id' not in order_message:
        logger.debug(order_message)
        raise Ignore(order_message)
    scripture = databases('scripture')
    u_result = scripture.g_orders.update_one(
        {
            'email': email,
            'message_id': order_message['message_id']
        },
        {
            '$set': order_message,
            '$setOnInsert': {
                'created_at': datetime.now()
            },
            '$currentDate': {
                'updated_at': True
            }
        },
        upsert=True
    )

    scripture.g_users.update_one(
        {
            'email': email
        },
        {
            '$currentDate':
            {
                'last_fetched_at': True,
                'updated_at': True
            }
        }
    )

    modified = u_result.raw_result.get('nModified') == 1 and \
        u_result.raw_result.get('ok') == 1

    sent_to_ai = False
    if u_result.upserted_id is not None:
        ai_endpoint = f'{ai_base}{mapping[order_message["category"]]}'
        headers = {'cache-control': 'no-cache'}
        data = order_message.copy()
        data['capture_id'] = u_result.upserted_id
        data['email'] = email
        resp = requests.post(ai_endpoint, data=data, headers=headers)
        sent_to_ai = True
        if resp.status_code != 200:
            sent_to_ai = False
            logger.error('Failed when sent to ai: %s', resp.text)

    return {
        'modified': modified,
        'is_updated': u_result.upserted_id is None,
        'is_inserted': u_result.upserted_id is not None,
        'sent_to_ai': sent_to_ai
    }


@app.task
def incremental_fetch(email: str) -> bool:
    """fetch more email"""
    scripture = databases('scripture')
    user = scripture.g_users.find_one({'email': email, 'authenticated': True})

    if not user:
        return False  # TODO: Add Dingtalk notify of other imformations

    do_request.apply_async(
        (email, user['access_token']),
        # TODO: only token, pop user's info
        link=dispatcher.s(email=email, token=user, uid=user['id'])
    )

    return True
