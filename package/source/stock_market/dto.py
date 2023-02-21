from dataclasses import dataclass
from typing import Dict

from stock_market.constants import Currency


@dataclass
class Rate:
    rate_at: str
    price: Dict[Currency, float]
