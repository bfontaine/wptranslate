#! /usr/bin/env python
# -*- coding: UTF-8 -*-

from __future__ import print_function

import argparse
import sys

from wptranslate import translate


def main():
    parser = argparse.ArgumentParser(description='Wikipedia-based Translator')
    parser.add_argument('languages', type=str,
            help='<source language>:<target language>, e.g.: fr:en')
    parser.add_argument('word', type=str, help='word or expression to translate')

    args = parser.parse_args()

    word = args.word
    source, target = args.languages.split(':')

    try:
        res = translate(word, source=source, target=target)
    except KeyboardInterrupt:
        return sys.exit(1)

    if res is None:
        print('No result for "%s" from %s to %s' % (word, source, target))
        return sys.exit(1)

    print(res)
