#!/usr/bin/python

def common_end(a, b):
    return ( a[0] == b[0] or a[-1] == b[-1] )


print common_end([1,2,3], [1,3])
