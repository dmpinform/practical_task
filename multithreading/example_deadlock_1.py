from threading import Thread, current_thread


def task(other):
    print(f'[{current_thread().name}] waiting on [{other.name}]...')
    other.join()


main_thread = current_thread()
new_thread = Thread(target=task, args=(main_thread, ))
new_thread.start()
task(new_thread)
