# coding: utf8

import asyncio


class Pool:

    def __init__(self, maxsize=1, loop=None):
        if not loop:
            loop = asyncio.get_event_loop()

        self._max_size = asyncio.Semaphore(value=maxsize, loop=loop)
        self._loop = loop
        self._clean()

    def _clean(self):
        self._counter = 0
        self._waiter = asyncio.futures.Future(loop=self._loop)

    def spawn(self, coro):
        assert asyncio.iscoroutine(coro), 'pool only accepts coroutine'

        async def limit():
            async with self._max_size as se:
                print(se)
                return await coro

        self._counter += 1

        future = asyncio.ensure_future(limit())
        future.add_done_callback(self._done)
        return future

    def _done(self, future):
        print('done')
        self._counter -= 1
        future.remove_done_callback(self._done)

        if self._counter <= 0:
            if not self._waiter.done():
                self.waiter.set_result(None)

    def join(self):
        def _on_complete(future):
            self._loop.stop()
            self._clean()

        self._waiter.add_done_callback(_on_complete)

        while self._counter > 0:
            if not self._loop.is_running():
                self._loop.run_forever()
