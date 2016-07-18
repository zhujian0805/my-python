#!/usr/bin/python
import time

a = "2013-10-10 23:40:00"
print a
timeArray = time.strptime(a, "%Y-%m-%d %H:%M:%S")
print timeArray
timeStamp = int(time.mktime(timeArray))
print timeStamp
