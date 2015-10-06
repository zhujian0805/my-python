#!/usr/bin/env python
import csv
import sys

f = open('01-csv.csv', 'r')

title = f.readline().strip().split(',')
#print title
#print len(title)

try:
    reader = csv.reader(f)
    for row in reader:
        for i in range(len(row)):
            print title[i] + ":" + row[i]
        print "\n"
finally:
    f.close()
