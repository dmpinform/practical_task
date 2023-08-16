import timeit
from threading import Thread

x = 0
add_counter = 0
subtract_counter = 0


def add_one():
    global x
    global add_counter
    for i in range(1000000):
        x += 1
        add_counter += 1


def subtract_one():
    global x
    global subtract_counter
    for i in range(1000000):
        x -= 1
        subtract_counter += 1


thread1 = Thread(target=add_one)
thread2 = Thread(target=subtract_one)

thread1.start()
thread2.start()

start = timeit.default_timer()
thread1.join()
thread2.join()
end = timeit.default_timer()
print(end - start)
print(x)
