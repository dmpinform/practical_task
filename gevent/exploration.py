from datetime import date

from gevent.io_methods import DatabaseIO, FileIO, HttpIO

fio = FileIO()
dbio = DatabaseIO()
httpio = HttpIO()

rates_jan = httpio.get_rate_by_period(
    date(2023, 1, 1),
    date(2023, 1, 30),
)
rates_feb = httpio.get_rate_by_period(
    date(2023, 2, 1),
    date(2023, 2, 28),
)

fio.write(rates_jan)
fio.write(rates_feb)

dbio.write(rates_jan)
dbio.write(rates_feb)

print(f'DB records: {fio.count()},  File records: {dbio.count()}')
