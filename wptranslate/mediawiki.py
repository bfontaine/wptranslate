#! /usr/bin/env python
# -*- coding: UTF-8 -*-

import requests

def query(params, lang='en'):
    """
    Simple Mediawiki API wrapper
    """

    url = 'https://%s.wikipedia.org/w/api.php' % lang
    finalparams = {
        'action': 'query',
        'format': 'json',
    }
    finalparams.update(params)

    resp = requests.get(url, params=finalparams)

    if not resp.ok:
        return None

    data = resp.json()
    if 'query' in data:
        return data['query']
