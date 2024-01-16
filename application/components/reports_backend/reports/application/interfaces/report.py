from abc import ABC, abstractmethod


class Reports(ABC):

    @abstractmethod
    def get_report(self, report_id: int) -> int:
        ...

    @abstractmethod
    def set_state(self, report_id: int, state: int) -> None:
        ...
