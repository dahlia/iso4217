from . import Currency


def test():
    assert Currency('USD') is Currency.USD
    assert Currency.USD.code == 'USD'
    assert Currency.USD.number == 840
    assert Currency.USD.currency_name == 'US Dollar'
    assert Currency.USD.country_names.issuperset(
        frozenset(['GUAM', 'UNITED STATES OF AMERICA (THE)'])
    )
    assert Currency.USD.exponent == 2
    assert Currency.usd is Currency.USD
    assert Currency('JPY') is Currency.JPY
    assert Currency.JPY.code == 'JPY'
    assert Currency.JPY.number == 392
    assert Currency.JPY.currency_name == 'Yen'
    assert Currency.JPY.country_names == frozenset(['JAPAN'])
    assert Currency.JPY.exponent == 0
    assert Currency.jpy is Currency.JPY


if __name__ == '__main__':
    test()
