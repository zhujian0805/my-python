#!/usr/bin/python

import Queue
myq = Queue.Queue()
from pprint import pprint


def fillQueue():
  fh = open("/etc/passwd")
  while True:
    line = fh.readline()
    if line:
      myq.put(line)
    else:
      break

fillQueue()
print myq.qsize()

i=1
while i <= 100000:
  fillQueue()
  i = i + 1

print myq.qsize()

j = 1
while j<100:
#while True:
  try:
    item = myq.get(block=False)
    print item
    j = j + 1
  except Empty:
    print "The Queue is empty!!!"
    break

print "Done"
