from dataclasses import asdict, dataclass
from datetime import date
from enum import Enum
from typing import Iterator, List

import requests

from package.stock_market import interfaces
from package.stock_market.adapters.exchangerate.settings import EXCHANGERATE_URI
from package.stock_market.constants import NODE_RATES, Currency
from package.stock_market.dto import Rate, RequestParams


@dataclass
class ExchangeRate(interfaces.Response):
    exchangerate_uri: str = EXCHANGERATE_URI

    def execute(self):
        return self._adapt_rates()

    def __post_init__(self):
        self.params = ExchangeRateParams()

    def _adapt_rates(self) -> Iterator[Rate]:
        rates = self._get_response()[NODE_RATES]

        for rate_at, price in rates.items():
            yield Rate(
                rate_at=rate_at,
                price=price,
            )

    def _get_response(self):
        return requests.get(
            url=self.exchangerate_uri,
            params=self.params.as_dict(),
        ).json()


class ExchangeRateParams:

    def __init__(self):
        self._params = RequestParams()

    def set_date_range(
            self, start_at: date, end_at: date,
    ) -> 'ExchangeRateParams':
        self._params.start_date = start_at.isoformat()
        self._params.end_date = end_at.isoformat()
        return self

    def set_currency(
            self, from_currency: Currency, to_currency: List[Currency]
    ) -> 'ExchangeRateParams':
        self._params.base = from_currency.value
        self._params.symbols = self._get_enum_values(to_currency)
        return self

    @staticmethod
    def _get_enum_values(list_enum: List[Enum]):
        return ','.join(list(map(lambda enum: enum.value, list_enum)))

    def as_dict(self):
        return asdict(self._params)
