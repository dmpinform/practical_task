import gevent

from gevente.explorations import http_io, period_jan
from gevente.tools.timer import timer


@timer
def call_one_thread():
    for step in range(1, 10):
        http_io.get_rate_by_period(*period_jan)


@timer
def call_with_gevent():
    threads = []
    for step in range(1, 10):
        rates_jan = gevent.spawn(http_io.get_rate_by_period, *period_jan)
        threads.append(rates_jan)

    gevent.joinall(threads)


call_one_thread()
call_with_gevent()
