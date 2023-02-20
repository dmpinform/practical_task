from abc import ABC, abstractmethod
from typing import List

from package.stock_market.dto import Rate


class Response(ABC):
    @abstractmethod
    def execute(self) -> List[Rate]:
        ...
