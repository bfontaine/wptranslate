#! /usr/bin/env python
# -*- coding: UTF-8 -*-

from wptranslate.mediawiki import query as mwquery

def get_page_title(text, lang=None):
    resp = mwquery({
        'list': 'search',
        'srsearch': text,
        'srinfo': 'suggestion',
        'srlimit': '1',
    }, lang=lang)

    if not resp or not resp.get('search'):
        return None

    return resp['search'][0]['title']


def translate(text, source, target, **kwargs):
    """
    Translate some ``text`` from a ``source`` language to a ``target`` one
    (both must be ISO codes). It starts by searching the text on Wikipedia in
    the source language, then find the equivalent page in the target language
    and return its title. If the page cannot be found, the function returns
    ``None``.

    >>> translate('Jambon', 'fr', 'en')
    u'Ham'
    """
    if not text:
        return None

    title  = get_page_title(text, source)

    if not title:
        return None

    resp = mwquery({
        'prop': 'langlinks',
        'lllang': target,
        'titles': title
    }, lang=source)

    if not resp or not resp.get('pages'):
        return None

    page = list(resp['pages'].values())[0]

    if 'langlinks' not in page:
        return None

    return page['langlinks'][0]['*']
