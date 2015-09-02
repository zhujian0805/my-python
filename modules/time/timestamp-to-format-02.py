#!/usr/bin/python

import time
import datetime

timeStamp = 1381419600

print timeStamp

dateArray = datetime.datetime.utcfromtimestamp(timeStamp)

print dateArray

otherStyleTime = dateArray.strftime("%d-%m-%Y %H:%M:%S")

print otherStyleTime
