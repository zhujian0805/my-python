#!/usr/bin/python

import datetime

now = datetime.datetime.now()

print now

otherStyleTime = now.strftime("%d-%m-%Y %H:%M:%S")

print otherStyleTime
