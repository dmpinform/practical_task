from threading import Lock, Thread

lock = Lock()
x = 0


def add_one(lock):
    global x
    for i in range(1000000):
        lock.acquire()
        x = x + 1
        lock.release()


def subtract_one(lock):
    global x
    for i in range(1000000):
        lock.acquire()
        x = x - 1
        lock.release()


thread2 = Thread(target=subtract_one, args=(lock, ))
thread1 = Thread(target=add_one, args=(lock, ))

thread1.start()
thread2.start()

thread1.join()
thread2.join()

print(x)
