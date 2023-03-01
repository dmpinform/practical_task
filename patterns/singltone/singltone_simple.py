from typing import List


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
