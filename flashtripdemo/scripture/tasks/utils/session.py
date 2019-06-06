# coding: utf8

from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import BackendApplicationClient

from tasks import settings


def session(token):
    """token is dict, must include access_token and token_type
    """
    client = BackendApplicationClient(client_id=settings.GOOGLE_CLIENT_ID)

    _session = OAuth2Session(
        client=client,
        client_id=settings.GOOGLE_CLIENT_ID,
        token=token,
    )
    _session.proxies = settings.PROXIES
    return _session
