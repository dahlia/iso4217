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


def test_pydantic():
    """Test Pydantic integration."""
    try:
        from pydantic import BaseModel
    except ImportError:
        print("Pydantic not installed, skipping pydantic tests")
        return

    # Test that Currency can be used in a Pydantic model without
    # arbitrary_types_allowed
    class Transaction(BaseModel):
        amount: float
        currency: Currency

    # Test validation from Currency instance
    t1 = Transaction(amount=100.0, currency=Currency.USD)
    assert t1.currency is Currency.USD
    assert t1.currency.code == 'USD'

    # Test validation from string value
    t2 = Transaction(amount=50.0, currency='EUR')
    assert t2.currency is Currency.EUR
    assert t2.currency.code == 'EUR'

    # Test serialization (model_dump)
    dumped = t1.model_dump()
    assert dumped['currency'] == 'USD'

    # Test JSON serialization
    json_str = t1.model_dump_json()
    assert '"currency":"USD"' in json_str

    # Test validation error for invalid currency
    try:
        Transaction(amount=100.0, currency='INVALID')
        assert False, "Should have raised validation error"
    except Exception:
        pass  # Expected

    # Test with lowercase currency code
    t3 = Transaction(amount=75.0, currency='jpy')
    assert t3.currency is Currency.JPY

    print("Pydantic tests passed!")


if __name__ == '__main__':
    test()
    test_pydantic()
