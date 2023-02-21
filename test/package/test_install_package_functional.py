from datetime import date

import pytest

from stock_market.adapters.exchangerate import ExchangeRate
from stock_market.adapters.exchangerate.params import ExchangeRateParams
from stock_market.constants import Currency
from stock_market.dto import Rate


@pytest.fixture(scope='module')
def result():
    eur = Currency.EUR.value
    rub = Currency.RUB.value
    return [
        Rate(rate_at='2023-01-01', price={eur: 0.935765, rub: 73.690876}),
        Rate(rate_at='2023-01-02', price={eur: 0.936622, rub: 72.43743}),
    ]


@pytest.fixture(scope='module')
def params():
    return ExchangeRateParams().set_date_range(
        start_at=date(2023, 1, 1),
        end_at=date(2023, 1, 2),
    ).set_currency(
        from_currency=Currency.USD,
        to_currency=[Currency.RUB, Currency.EUR, ]
    )


def test_exchange_rate(result, params):
    rates = ExchangeRate(params).execute()
    assert list(rates) == result
