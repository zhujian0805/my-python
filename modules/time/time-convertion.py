#!/usr/bin/python
import time

a = "2013-10-10 23:40:00"
print a
timeArray = time.strptime(a, "%Y-%m-%d %H:%M:%S")
print timeArray
otherStyleTime = time.strftime("%Y/%m/%d %H:%M:%S", timeArray)
print otherStyleTime
