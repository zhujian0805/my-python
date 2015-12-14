#!/usr/bin/python
from multiprocessing import Process, Queue
import time

def worker(input):
    for i in iter(input.get, 'STOP'):
        print "dequeue %s" % i
        time.sleep(5)


def main():
    processes = []
    NUMBER_OF_PROCESSES = 20

    task_queue = Queue()

    for i in range(100):
            task_queue.put(str(i))

    for i in range(NUMBER_OF_PROCESSES):
        p = Process(target=worker, args=(task_queue, )).start()
        processes.append(p)

    while not task_queue.empty():
        time.sleep(1)

    for i in range(NUMBER_OF_PROCESSES):
        print 'put in %d STOP' % i
        task_queue.put('STOP')

if __name__ == '__main__':
    main()
