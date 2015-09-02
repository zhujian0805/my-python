#!/usr/bin/python
import time

timeStamp = 1381419600

print timeStamp

timeArray = time.localtime(timeStamp)

print timeArray

otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)

print otherStyleTime
