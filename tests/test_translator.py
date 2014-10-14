# -*- coding: UTF-8 -*-

import responses
from helpers import TestCase

from wptranslate.translator import get_page_title, translate


class TestTranslator(TestCase):

    def setUp(self):
        self.lang = 'foo'
        self.url = 'https://%s.wikipedia.org/w/api.php' % self.lang
        self.responses = []

    def add_resp(self, code, body):
        self.responses.append((code, {}, body))

    def mk_resps_callback(self):
        return lambda r: self.responses.pop(0)


    @responses.activate
    def test_get_page_title_return_none_on_error(self):
        responses.add(responses.GET, self.url, body='{}', status=404)
        self.assertNone(get_page_title("x", lang=self.lang))
        self.assertEquals(1, len(responses.calls))

    @responses.activate
    def test_get_page_title_return_none_on_wrong_resp(self):
        responses.add(responses.GET, self.url, body='{}', status=200)
        self.assertNone(get_page_title("x", lang=self.lang))
        self.assertEquals(1, len(responses.calls))

    @responses.activate
    def test_get_page_title_return_none_on_wrong_resp_query(self):
        body = '{"query": {}}'
        responses.add(responses.GET, self.url, body=body, status=200)
        self.assertNone(get_page_title("x", lang=self.lang))
        self.assertEquals(1, len(responses.calls))

    @responses.activate
    def test_get_page_title(self):
        title = 'fooqz+_a123q'
        body = '{"query": {"search":[{"title":"%s"}]}}' % title
        responses.add(responses.GET, self.url, body=body, status=200)
        self.assertEquals(title, get_page_title("x", lang=self.lang))
        self.assertEquals(1, len(responses.calls))

    @responses.activate
    def test_translate_none(self):
        self.assertNone(translate(None, 'en', 'es'))
        self.assertEquals(0, len(responses.calls))

    @responses.activate
    def test_translate_wrong_title(self):
        responses.add(responses.GET, self.url, body='{}', status=200)
        self.assertNone(translate("x", self.lang, 'es'))
        self.assertEquals(1, len(responses.calls))

    @responses.activate
    def test_translate_good_title_wrong_query(self):
        title = 'fooqz+_a123q'
        self.add_resp(200, '{"query": {"search":[{"title":"%s"}]}}' % title)
        self.add_resp(404, '{}')
        cb = self.mk_resps_callback()
        responses.add_callback(responses.GET, self.url, callback=cb)
        self.assertNone(translate("x", self.lang, 'es'))
        self.assertEquals(2, len(responses.calls))

    @responses.activate
    def test_translate_good_title_no_langlink(self):
        title = 'fooqz+_a123q'
        titlebody = '{"query": {"search":[{"title":"%s"}]}}' % title
        pagebody = '{"query": {"pages": {"foo": {}}}}'
        self.add_resp(200, titlebody)
        self.add_resp(200, pagebody)
        cb = self.mk_resps_callback()
        responses.add_callback(responses.GET, self.url, callback=cb)
        self.assertNone(translate("x", self.lang, 'es'))
        self.assertEquals(2, len(responses.calls))
        self.assertEquals(titlebody, responses.calls[0].response.text)
        self.assertEquals(pagebody, responses.calls[1].response.text)

    @responses.activate
    def test_translate_good_title_with_langlinks(self):
        title = 'fooqz+_a123q'
        word = 'qa2f*$&x0'
        titlebody = '{"query": {"search":[{"title":"%s"}]}}' % title
        pagebody = '''{"query":
            {"pages": {"foo": {"langlinks":[{"*":"%s"}]}}}}''' % word
        self.add_resp(200, titlebody)
        self.add_resp(200, pagebody)
        cb = self.mk_resps_callback()
        responses.add_callback(responses.GET, self.url, callback=cb)
        self.assertEquals(word, translate("x", self.lang, 'es'))
        self.assertEquals(2, len(responses.calls))
        self.assertEquals(titlebody, responses.calls[0].response.text)
        self.assertEquals(pagebody, responses.calls[1].response.text)
