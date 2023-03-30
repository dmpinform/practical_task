import gevent

from gevente.explorations import http_io, period_jan
from gevente.tools.methods import FileIO
from gevente.tools.timer import timer

rates_jan_ = http_io.get_rate_by_period(*period_jan)
rates_jan = rates_jan_
for i in range(1, 10):
    rates_jan = rates_jan + rates_jan_


@timer
def call_one_thread():
    for step in range(1, 10):
        file_one = FileIO(f'one_{step}.txt')
        file_one.write(rates_jan)


@timer
def call_with_gevent():
    green_threads = []
    for step in range(1, 10):
        file_two = FileIO(f'two_{step}.txt')
        green_threads.append(gevent.spawn(file_two.write, rates_jan))

    gevent.joinall(green_threads)


call_one_thread()
call_with_gevent()
