# -*- coding: UTF-8 -*-

try:
    import unittest2 as unittest
except ImportError:
    import unittest


class TestCase(unittest.TestCase):
    """
    Enhanced ``unittest.TestCase``
    """

    def assertNone(self, expr):
        return self.assertIs(expr, None)
