# coding: utf8

from sanic_session import InMemorySessionInterface


class Session:
    def __init__(self, app, interface=InMemorySessionInterface()):
        self.session_interface = interface
        self.app = app

        app.middleware('request')(self.on_request_start)
        app.middleware('response')(self.on_response_complete)

    async def on_request_start(self, request):
        # before each request initialize a session
        # using the client's request
        await self.session_interface.open(request)

    async def on_response_complete(self, request, response):
        # after each request save the session,
        # pass the response to set client cookies
        await self.session_interface.save(request, response)
