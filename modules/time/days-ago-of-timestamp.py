#!/usr/bin/python
import time
import datetime

timeStamp = 1381419600

print timeStamp

dateArray = datetime.datetime.utcfromtimestamp(timeStamp)

print dateArray

threeDayAgo = dateArray - datetime.timedelta(days = 3)

print threeDayAgo
