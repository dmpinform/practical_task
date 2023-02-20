from abc import ABC, abstractmethod


class EngineBase(ABC):
    @abstractmethod
    def get_info(self) -> str:
        ...
