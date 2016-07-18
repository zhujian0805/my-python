#!/usr/bin/python

def last2(str):
    count = 0
    last2 = str[-2:]
    for i in xrange(0,len(str)-2):
        s = str[i:i+2]
        if s == last2:
            count = count + 1
    return count

print last2('aasljdfaaa')
