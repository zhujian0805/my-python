#!/usr/bin/python

import time

import datetime

threeDayAgo = (datetime.datetime.now() - datetime.timedelta(days=3))

print threeDayAgo

timeStamp = int(time.mktime(threeDayAgo.timetuple()))

print timeStamp

otherStyleTime = threeDayAgo.strftime("%d-%m-%Y %H:%M:%S")

print otherStyleTime
