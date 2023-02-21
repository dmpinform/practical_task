from dataclasses import dataclass
from typing import Dict

from package.stock_market.constants import Currency


@dataclass
class Rate:
    rate_at: str
    price: Dict[Currency, float]
