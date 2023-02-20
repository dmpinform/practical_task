from datetime import date

from stock_market.adapters.exchangerate import ExchangeRate
from stock_market.constants import Currency


def test_exchange_rate():
    rates = ExchangeRate()
    rates.params.set_date_range(
        start_at=date(2023, 1, 1),
        end_at=date(2023, 1, 2),
    ).set_currency(
        from_currency=Currency.USD,
        to_currency=[Currency.RUB, Currency.EUR, ]
    )

    result = rates.execute()
