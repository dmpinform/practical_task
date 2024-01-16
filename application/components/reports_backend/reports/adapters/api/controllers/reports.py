from dataclasses import dataclass

from reports.application import services


@dataclass
class Reports:
    report: services.Reports

    def upload(self, report_id: int):
        return self.report.create(report_id)
