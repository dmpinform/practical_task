import gevent

from gevente.explorations import file_io, http_io, period_feb, period_jan
from gevente.tools.timer import timer


@timer
def call_one_thread():
    rates_jan = http_io.get_rate_by_period(*period_jan)
    rates_feb = http_io.get_rate_by_period(*period_feb)

    file_io.write(rates_jan)
    file_io.write(rates_feb)


@timer
def call_with_gevent():
    rates_jan = gevent.spawn(http_io.get_rate_by_period, *period_jan)
    rates_feb = gevent.spawn(http_io.get_rate_by_period, *period_feb)

    results = gevent.joinall([rates_jan, rates_feb])

    for rate in results:
        file_io.write(rate.value)


call_one_thread()
call_with_gevent()
