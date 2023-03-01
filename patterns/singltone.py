from typing import List


# вариант использования для глобального буфера
class AbstractStorage(object):
    _instance = None
    messages: List[str] = []

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance


a1 = AbstractStorage()
a2 = AbstractStorage()
a3 = AbstractStorage()
a1.messages.append('111')
a2.messages.append('222')
a3.messages.append('333')
print(id(a1) == id(a2) == id(a3))
print(a1.messages)
print(a1.messages)


class SingletonMeta(type):
    _instance = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instance:
            instance = super().__call__(*args, **kwargs)
            cls._instance[cls] = instance

        return cls._instance[cls]


class Singleton(metaclass=SingletonMeta):

    def some_logic(self):
        pass


# вариант использования для глобального справочника
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
