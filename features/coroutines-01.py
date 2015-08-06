#!/usr/bin/python

def receiver():
  print "Ready to receive"
  while True:
    n = (yield)
    print "Got %s" % n


r = receiver()
r.next()
r.send(1)
r.send(2)
r.send(3)
r.send(4)
r.send("Hello buddy!!!")
