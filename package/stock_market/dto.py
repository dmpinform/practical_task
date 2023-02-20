from dataclasses import dataclass
from typing import Dict

from package.stock_market.constants import Currency


@dataclass
class Rate:
    rate_at: str
    price: Dict[Currency, float]


@dataclass(init=False)
class RequestParams:
    start_date: str
    end_date: str
    base: str
    symbols: Dict[str, float]
