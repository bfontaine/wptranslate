# -*- coding: UTF-8 -*-

import responses
from helpers import TestCase

from wptranslate.mediawiki import query

class TestMediaWiki(TestCase):

    def setUp(self):
        self.lang = 'foo'
        self.url = 'https://%s.wikipedia.org/w/api.php' % self.lang


    @responses.activate
    def test_query_return_none_on_error(self):
        responses.add(responses.GET, self.url, body='{}', status=404)
        self.assertNone(query({}, lang=self.lang))
        self.assertEquals(1, len(responses.calls))

    @responses.activate
    def test_query_return_none_on_wrong_resp(self):
        responses.add(responses.GET, self.url, body='{}', status=200)
        self.assertNone(query({}, lang=self.lang))
        self.assertEquals(1, len(responses.calls))

    @responses.activate
    def test_query_return_query_param(self):
        responses.add(responses.GET, self.url, body='{"query": 42}', status=200)
        self.assertEquals(42, query({}, lang=self.lang))
        self.assertEquals(1, len(responses.calls))
