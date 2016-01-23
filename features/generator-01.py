#!/usr/bin/python
import sys


def countdown(n):
    print "Counting down from %d" % n
    while n > 0:
        yield n
        n -= 1
    return


n = countdown(10)
while True:
    try:
        i = n.next()
        if i:
            print i
        else:
            break
    except:
        sys.exit(0)
