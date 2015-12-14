#!/usr/bin/python
from multiprocessing import Process, Queue
from Queue import Empty

q = Queue()

def consumer_worker(q):
    while True:
        try:
            item = q.get(block=False)
            print item
        except Empty:
            print "The Queue is empty!!!"
            break

def producer_worker(q):
    for i in xrange(1,100):
        q.put("Hello World!!!")
    
p = Process(target=producer_worker, args=(q,))
p.start()
p.join()

p1 = Process(target=consumer_worker, args=(q,))
p1.start()
p1.join()

exit()
