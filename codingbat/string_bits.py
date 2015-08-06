#!/usr/bin/python

def string_bits(str):
    ss = ''
    for i in xrange(0,len(str)):
        if i%2 == 0:
            ss = ss + str[i]
    return ss

print string_bits('Hello')
