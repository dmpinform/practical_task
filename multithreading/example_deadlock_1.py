# example of a deadlock caused by threads waiting on each other
from threading import Thread, current_thread


# task to be executed in a new thread
def task(other):
    # message
    print(f'[{current_thread().name}] waiting on [{other.name}]...')
    other.join()


# get the current thread
main_thread = current_thread()
# create the second thread
new_thread = Thread(target=task, args=(main_thread, ))
# start the new thread
new_thread.start()
# run the first thread
task(new_thread)
