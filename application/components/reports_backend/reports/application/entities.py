from dataclasses import dataclass
from datetime import datetime


@dataclass
class Reports:
    id: int
    name: str
    start_at: datetime
    end_at: datetime
