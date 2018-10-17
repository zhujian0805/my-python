#!/usr/bin/python
""" This is a sample for os.fork"""
import os, time, sys

PID = os.fork()
CHILDREN = []

if PID != 0:
    CHILDREN.append(PID)
else:
    time.sleep(5)
    sys.exit(0)

(PID, STATUS) = os.waitpid(PID, 0)

print str(PID) + "\t" + str(STATUS)
sys.exit(0)
