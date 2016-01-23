#!/usr/bin/python
import sys


def countdown(n):
    print "Counting down from %d" % n
    while n > 0:
        yield n
        n -= 1
    return


for i in countdown(10):
    print i
