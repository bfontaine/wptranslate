wptranslate
===========

.. image:: https://img.shields.io/travis/bfontaine/wptranslate.png
   :target: https://travis-ci.org/bfontaine/wptranslate
   :alt: Build status

.. image:: https://coveralls.io/repos/bfontaine/wptranslate/badge.png?branch=master
   :target: https://coveralls.io/r/bfontaine/wptranslate?branch=master
   :alt: Coverage status

``wptranslate`` is a command-line translator tool based on Wikipedia.

Install
-------

.. code-block::
    pip install wptranslate

Usage
-----

.. code-block::
    wptranslate [-s <source language>] [-t <target language>] <word>


Example
~~~~~~~

.. code-block::
    $ wptranslate -s fr -t en jambon
    Ham
