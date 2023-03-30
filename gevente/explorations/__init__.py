# flake8: noqa
from datetime import date

from gevent import monkey

monkey.patch_all()

from gevente.tools.methods import FileIO, HttpIO

file_io = FileIO()
http_io = HttpIO()
period_jan = (date(2023, 1, 1), date(2023, 1, 30))
period_feb = (date(2023, 2, 1), date(2023, 2, 28))

__all__ = (file_io, http_io, period_jan, period_feb)
