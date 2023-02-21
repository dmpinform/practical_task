from dataclasses import asdict
from datetime import date
from enum import Enum
from typing import List

from stock_market import interfaces
from stock_market.adapters.exchangerate.dto import RequestParams
from stock_market.constants import Currency


class ExchangeRateParams(interfaces.Params):

    def __init__(self):
        self._params = RequestParams()

    def as_dict(self):
        return asdict(self._params)

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
