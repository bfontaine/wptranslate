# -*- coding: UTF-8 -*-

try:
    import unittest2 as unittest
except ImportError:
    import unittest

import responses

from wptranslate.mediawiki import query

class TestMediaWiki(unittest.TestCase):

    def assertNone(self, expr):
        return self.assertIs(expr, None)


    @responses.activate
    def test_query_return_none_on_error(self):
        responses.add(responses.GET, 'https://foo.wikipedia.org/w/api.php',
                body='{}', status=404)
        self.assertNone(query({}, lang='foo'))
        self.assertEquals(1, len(responses.calls))

    @responses.activate
    def test_query_return_none_on_wrong_resp(self):
        responses.add(responses.GET, 'https://foo.wikipedia.org/w/api.php',
                body='{}', status=200)
        self.assertNone(query({}, lang='foo'))
        self.assertEquals(1, len(responses.calls))

    @responses.activate
    def test_query_return_query_param(self):
        responses.add(responses.GET, 'https://foo.wikipedia.org/w/api.php',
                body='{"query": 42}', status=200)
        self.assertEquals(42, query({}, lang='foo'))
        self.assertEquals(1, len(responses.calls))
