import logging
import time

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)


def timer(func):

    def wrapper(*args, **kwargs):
        start = time.time()
        call_func = func(*args, **kwargs)
        end = time.time()
        result = start - end
        logging.info(f'{func.__name__} time = {result}')
        return call_func

    return wrapper
