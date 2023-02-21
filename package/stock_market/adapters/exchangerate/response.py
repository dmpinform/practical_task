from typing import Iterator

from package.stock_market.adapters.base.response import ResponseBase
from package.stock_market.adapters.exchangerate.params import ExchangeRateParams
from package.stock_market.adapters.exchangerate.settings import (
    EXCHANGERATE_URI,
    NODE_RATES,
)
from package.stock_market.dto import Rate


class ExchangeRate(ResponseBase):

    def __init__(self, params: ExchangeRateParams):
        super().__init__(
            params=params.as_dict(),
            uri=EXCHANGERATE_URI,
        )

    def adapt(self) -> Iterator[Rate]:
        rates = self.get_response()[NODE_RATES]

        for rate_at, price in rates.items():
            yield Rate(
                rate_at=rate_at,
                price=price,
            )
