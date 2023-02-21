from abc import ABC, abstractmethod
from typing import Any, Iterator, Mapping

from stock_market.dto import Rate


class Response(ABC):
    @abstractmethod
    def execute(self) -> Iterator[Rate]:
        ...


class Params(ABC):
    @abstractmethod
    def as_dict(self) -> Mapping[str, Any]:
        ...
