from datetime import date
from typing import List

from stock_market.adapters.exchangerate import ExchangeRate
from stock_market.adapters.exchangerate.params import ExchangeRateParams
from stock_market.constants import Currency
from stock_market.dto import Rate

from gevente.tools.adapters import RateFile
from gevente.tools.constants import RATES_DEFAULT_FILE


class FileIO:

    def __init__(self, file_rates: str = RATES_DEFAULT_FILE):
        self.RateFile = RateFile(file_rates)

    def write(self, rates: List[Rate]):
        self.RateFile.write(rates)

    def read(self):
        self.RateFile.read()

    def count(self) -> int:
        return self.RateFile.count()


class HttpIO:

    @staticmethod
    def get_rate_by_period(start_at: date, end_at: date):
        params = ExchangeRateParams().set_date_range(
            start_at=start_at, end_at=end_at
        ).set_currency(
            from_currency=Currency.USD,
            to_currency=[
                Currency.RUB,
                Currency.EUR,
            ]
        )
        return list(ExchangeRate(params).execute())
