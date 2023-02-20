from typing import List

from iterator.entities import BaseProduct


class Cart:
    def __init__(self, *product):
        self._cart: List[BaseProduct] = [*product]
        self._pos: int = -1

    def put(self, product: BaseProduct) -> None:
        self._cart.append(product)

    def __iter__(self):
        return self

    def __next__(self):
        self._pos += 1
        if self._pos < len(self._cart):
            return self._cart[self._pos]
        else:
            raise StopIteration

    def get_count_product(self) -> int:
        return len(self._cart)
