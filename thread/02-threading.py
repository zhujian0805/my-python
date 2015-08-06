#!/usr/bin/env python
import Queue
import threading
import time
import sys

# Subclassing my own threading.Thread class
class myThread(threading.Thread):
    def __init__(self, threadID, taskq):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.q = taskq
    
    def run(self):
#        print "Starting processing data"
        working_on_thing(self.threadID, self.q)
#        print "Stopping processing data"

# This is the real worker
def working_on_thing(tid, q):
    for i in iter(q.get, 'STOP'):
        count = 0;
        if i == 2:
            sys.exit(100)
        while count <=3:
            print "thread %s, is still running at count %s for data %s" % ( str(tid), str(count), str(i) )
            count = count + 1

# create task queue, and put tasks in queue
task_queue = Queue.Queue()
for i in range(100):
    task_queue.put(i)

# Start 10 worker thread
for tid in range(10):
    thread = myThread(tid, task_queue)
    thread.start()

# Since we started 10 thread, so we need 3 'STOP' to stop them
for i in range(10):
    task_queue.put('STOP')


print "All thread finished working"
