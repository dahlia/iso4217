``iso4217``: Currency data package for Python
=============================================

.. image:: https://badge.fury.io/py/iso4217.svg?
   :target: https://pypi.python.org/pypi/iso4217
.. image:: https://github.com/dahlia/iso4217/actions/workflows/main.yaml/badge.svg
   :target: https://github.com/dahlia/iso4217/actions/workflows/main.yaml

This Python package contains `ISO 4217`_ currency data, represented as
enum_ module which was introduced in 3.4.

>>> from iso4217 import Currency
>>> Currency.USD
<Currency.USD: 'USD'>
>>> Currency.USD.code
'USD'
>>> Currency.USD.currency_name
'US Dollar'
>>> Currency.USD.exponent  # USD has cents
2
>>> Currency.JPY
<Currency.JPY: 'JPY'>
>>> Currency.JPY.currency_name
'Yen'
>>> Currency.JPY.exponent  # JPY has no minor units
0
>>> Currency('KRW')  # Get by the code string
<Currency.KRW: 'KRW'>
>>> Currency.KRW is Currency('KRW')
True
>>> Currency.krw is Currency.KRW  # Lower enumerants are also available

Written by `Hong Minhee`_.  Distributed under Public Domain.


.. _ISO 4217: http://www.iso.org/iso/home/standards/currency_codes.htm
.. _enum: https://docs.python.org/3/library/enum.html
.. _enum34: https://pypi.python.org/pypi/enum34
.. _Hong Minhee: https://hongminhee.org/
