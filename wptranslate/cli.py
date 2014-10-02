#! /usr/bin/env python
# -*- coding: UTF-8 -*-

from __future__ import print_function

import argparse
import sys

from wptranslate import translate


def main():
    parser = argparse.ArgumentParser(description='Wikipedia-based Translator')
    parser.add_argument('word', type=str, help='word or expression to translate')
    parser.add_argument('-s', '--source', dest='source', type=str,
            help='source language')
    parser.add_argument('-t', '--target', dest='target', type=str,
            help='destination language')
    args = parser.parse_args()

    word, source, target = args.word, args.source, args.target

    try:
        res = translate(word, source=source, target=target)
    except KeyboardInterrupt:
        pass

    if res is None:
        print('No result for "%s" from %s to %s' % (word, source, target))
        return sys.exit(1)

    print(res)
