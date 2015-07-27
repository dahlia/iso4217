from . import Currency


def test():
    assert Currency.usd.code == 'USD'
    assert Currency.usd.number == 840
    assert Currency.usd.currency_name == 'US Dollar'
    assert Currency.usd.country_names.issuperset(
        frozenset(['GUAM', 'UNITED STATES OF AMERICA (THE)'])
    )
    assert Currency.usd.exponent == 2
    assert Currency.jpy.code == 'JPY'
    assert Currency.jpy.number == 392
    assert Currency.jpy.currency_name == 'Yen'
    assert Currency.jpy.country_names == frozenset(['JAPAN'])
    assert Currency.jpy.exponent == 0


if __name__ == '__main__':
    test()
