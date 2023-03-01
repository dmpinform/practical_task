# вариант использования для глобального справочника
from typing import List


class TransactionContextManager:
    _rows: List[int] = None

    @classmethod
    def get_rows(cls):

        if not cls._rows:
            cls._rows = cls._get_rows()

        return cls._rows

    @classmethod
    def _get_rows(cls) -> List[int]:
        print('FILL ROWS')
        return [1, 2, 3]


t1 = TransactionContextManager().get_rows()
t2 = TransactionContextManager().get_rows()
print(id(t1) == id(t2))
print(t1, t2)
