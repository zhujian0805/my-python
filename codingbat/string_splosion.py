#!/usr/bin/python
import sys

def string_splosion(str):
    s = ''
    for i in xrange(0, len(str)):
        s = s + str[:i+1] 
    return s

print string_splosion('abcd')
