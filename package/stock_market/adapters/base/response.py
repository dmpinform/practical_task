from abc import abstractmethod
from typing import Any, Iterator, Mapping

import requests

from package.stock_market import interfaces


class ResponseBase(interfaces.Response):

    def __init__(self, params: Mapping[str, Any], uri: str):
        self.params = params
        self.uri = uri

    def execute(self):
        return self.adapt()

    @abstractmethod
    def adapt(self) -> Iterator:
        ...

    def get_response(self):
        return requests.get(
            url=self.uri,
            params=self.params,
        ).json()
