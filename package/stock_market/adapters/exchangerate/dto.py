from dataclasses import dataclass
from typing import Dict


@dataclass(init=False)
class RequestParams:
    start_date: str
    end_date: str
    base: str
    symbols: Dict[str, float]
