# coding: utf8
"""
TestCase
Created by: songww
"""

from tasks.gnews import make_requests, news_with_loc, news_with_topic


class TestGNews(object):

    def test_make_requests(self):
        make_requests.delay()

    def test_fetch(self):
        fetch = news_with_loc.delay('New York, US')
        fetch.wait()
        assert fetch.state == 'SUCCESS'
        result = fetch.get()
        assert result is True


if __name__ == '__main__':
    TestGNews().test_fetch()
