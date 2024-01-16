from reports.adapters.database.transaction.base_repository import BaseRepository
from reports.application import interfaces


class ReportsRepo(interfaces.Reports, BaseRepository):

    def get_report(self, report_id: int) -> int:
        ...

    def set_state(self, report_id: int, state: int) -> None:
        ...
