#!/usr/bin/python
# coding=UTF-8

fh = open("/tmp/test.txt", "w")

string = u'我是中国人'
fh.write("我是中国人")
fh.close()

fh = open("/tmp/test.txt", "r")
lines = fh.readlines()
print "1:>"
print lines
print "2:>"
print lines[0]
fh.close()

fh = open("/tmp/test.txt", "r")
while True:
    line = fh.readline()
    if line:
        print "3:>"
        print line
    else:
        break
fh.close()
