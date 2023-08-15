from threading import Thread

x = 0


def add_one():
    global x
    for i in range(1000000):
        x += 1


def subtract_one():
    global x
    for i in range(1000000):
        x -= 1


thread1 = Thread(target=add_one)
thread2 = Thread(target=subtract_one)

thread1.start()
thread2.start()

thread1.join()
thread2.join()

print(x)
