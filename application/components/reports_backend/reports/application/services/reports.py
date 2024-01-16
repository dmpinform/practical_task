from dataclasses import dataclass

from reports.adapters.broker.pub import Pub
from reports.application import interfaces
from reports.application.transaction import context_db_app


@dataclass
class Reports:
    reports_repo: interfaces.Reports
    pub: Pub

    def _send_signal(self, message: str):
        self.pub.send_message(message, 'reports_for_generation')

    def _completed_report_signal(self, user_id):
        self.pub.set_tmp_user_channel('user_2')
        self.pub.send_message('report_id=2', user_id)

    @context_db_app
    def create(self, report_id: int) -> int:
        self._send_signal(f'report_id: {report_id}')
        return self.reports_repo.get_report(report_id)

    def generate(self, body):
        print('generate', body)
        user_id = 'user_2'
        self._completed_report_signal(user_id)

    @context_db_app
    def set_step(self) -> None:
        return self.reports_repo.set_state(report_id=1, state=1)
