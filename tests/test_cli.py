# -*- coding: UTF-8 -*-

import responses
import sys

try:
    from cStringIO import StringIO
except ImportError:  # Python 3
    from io import StringIO

from helpers import TestCase

from wptranslate.cli import main

class TestCli(TestCase):

    def setUp(self):
        self.sys_argv = sys.argv
        self.sys_exit = sys.exit
        self.exit_code = None
        def _fake_exit(code=None):
            self.exit_code = code
        _fake_exit.__name__ = sys.exit.__name__
        sys.exit = _fake_exit
        self.sys_stdout, self.sys_stderr = sys.stdout, sys.stderr
        self.lang = 'foo'
        self.url = 'https://%s.wikipedia.org/w/api.php' % self.lang
        self.responses = []

    def tearDown(self):
        sys.argv = self.sys_argv
        sys.exit = self.sys_exit
        sys.stdout, sys.stderr = self.sys_stdout, self.sys_stderr

    def add_resp(self, code, body):
        self.responses.append((code, {}, body))

    def mk_resps_callback(self):
        return lambda r: self.responses.pop(0)

    def silent(self):
        """ remove any output from the rest of the test """
        sys.stdout, sys.stderr = StringIO(), StringIO()


    @responses.activate
    def test_abort_on_keyboard_interrupt(self):
        def ctrlC(*args, **kw):
            raise KeyboardInterrupt()

        responses.add_callback(method=responses.GET, url=self.url, callback=ctrlC)
        sys.argv = ['wptranslate', '%s:en' % self.lang, 'myword']
        self.assertNone(self.exit_code)
        main()
        self.assertEquals(1, self.exit_code)

    @responses.activate
    def test_error_if_no_result(self):
        responses.add(method=responses.GET, url=self.url, body='{}')
        sys.argv = ['wptranslate', '%s:en' % self.lang, 'myword']
        self.assertNone(self.exit_code)
        self.silent()
        main()
        self.assertEquals(1, self.exit_code)

    @responses.activate
    def test_success(self):
        title = 'fooqz+_a123q'
        word = 'qa2f*$&x0'
        titlebody = '{"query": {"search":[{"title":"%s"}]}}' % title
        pagebody = '''{"query":
            {"pages": {"foo": {"langlinks":[{"*":"%s"}]}}}}''' % word
        self.add_resp(200, titlebody)
        self.add_resp(200, pagebody)
        cb = self.mk_resps_callback()
        responses.add_callback(responses.GET, self.url, callback=cb)
        sys.argv = ['wptranslate', '%s:en' % self.lang, 'myword']
        self.assertNone(self.exit_code)
        self.silent()
        main()
        self.assertNone(self.exit_code)
        self.assertEquals(2, len(responses.calls))
        self.assertEquals(titlebody, responses.calls[0].response.text)
        self.assertEquals(pagebody, responses.calls[1].response.text)
        sys.stdout.seek(0)
        self.assertEquals(word, sys.stdout.read().strip())
