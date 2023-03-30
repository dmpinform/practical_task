import os
from typing import List

from stock_market.constants import Currency
from stock_market.dto import Rate


class RateFile:

    def __init__(self, file_name: str):
        self.file_rates = file_name
        if os.path.exists(self.file_rates):
            os.remove(self.file_rates)

    def write(self, rates: List[Rate]):
        with open(self.file_rates, 'a') as _file:
            for rate in rates:
                record = self._adapt_record(rate)
                _file.write(record)

    @staticmethod
    def _adapt_record(rate):
        return f'{rate.rate_at}; {rate.price[Currency.EUR.value]}\n'

    def count(self) -> int:
        lines = 0
        with open(self.file_rates, 'r') as _file:
            for _ in _file:
                lines += 1
        return lines
