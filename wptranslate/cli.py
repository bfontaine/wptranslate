#! /usr/bin/env python
# -*- coding: UTF-8 -*-

from __future__ import print_function

import argparse
from wptranslate import translate


def main():
    parser = argparse.ArgumentParser(description='Wikipedia-based Translator')
    parser.add_argument('word', type=str, help='word or expression to translate')
    parser.add_argument('-s', '--source', dest='source_lang', type=str,
            help='source language')
    parser.add_argument('-t', '--to', dest='to_lang', type=str,
            help='destination language')
    args = parser.parse_args()

    try:
        print(translate(args.word, source=args.source_lang, dest=args.to_lang))
    except KeyboardInterrupt:
        pass
