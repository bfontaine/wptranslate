wptranslate
===========

.. image:: https://img.shields.io/travis/bfontaine/wptranslate.png
   :target: https://travis-ci.org/bfontaine/wptranslate
   :alt: Build status

.. image:: https://coveralls.io/repos/bfontaine/wptranslate/badge.png?branch=master
   :target: https://coveralls.io/r/bfontaine/wptranslate?branch=master
   :alt: Coverage status

``wptranslate`` is a command-line translator tool based on Wikipedia.

It should be used for concepts and vague topics where a typical translator tool
wouldn’t give an accurate translation, but not for other things. For example,
you won’t be able to translate a whole sentence with it.


Install
-------

.. code-block::

    pip install wptranslate


Usage
-----

.. code-block::

    wptranslate <source language>:<target language> <word>


Example
~~~~~~~

.. code-block::

    $ wptranslate fr:en jambon
    Ham
