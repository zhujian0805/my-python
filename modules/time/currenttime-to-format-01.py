#!/usr/bin/python

import time

now = int(time.time())

print now

timeArray = time.localtime(now)

print timeArray

otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)

print otherStyleTime
