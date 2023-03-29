import os
from datetime import date
from typing import List

from sqlalchemy import func, insert, select
from stock_market.adapters.exchangerate import ExchangeRate
from stock_market.adapters.exchangerate.params import ExchangeRateParams
from stock_market.constants import Currency
from stock_market.dto import Rate

from gevent.database import get_engine, rate_table


class FileIO:

    def __init__(self):
        self.file_rates = 'rates.txt'
        if os.path.exists(self.file_rates):
            os.remove(self.file_rates)

    def write(self, rates: List[Rate]):
        with open(self.file_rates, 'a') as _file:
            for rate in rates:
                record = f'{rate.rate_at}; {rate.price[Currency.EUR.value]}\n'
                _file.write(record)

    def count(self) -> int:
        lines = 0
        with open(self.file_rates, 'r') as _file:
            for _ in _file:
                lines += 1
        return lines


class DatabaseIO:

    def __init__(self):
        self.connect = get_engine().connect()

    def write(self, rates: List[Rate]):
        for rate in rates:
            self.connect.execute(
                insert(rate_table).values(
                    {
                        'rate_at': rate.rate_at,
                        'price': rate.price[Currency.EUR.value]
                    }
                )
            )

    def count(self) -> int:
        stmt_select = select(func.count(rate_table.c.id))
        result = self.connect.execute(stmt_select).scalar()
        return result


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
