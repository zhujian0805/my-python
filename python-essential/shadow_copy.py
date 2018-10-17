#!/usr/bin/python

a = [1, 2, [12, 32], 3]

b = list(a)

if b is a:
    print "YES"

b.append(100)

print b

print a

b[2][0] = -10000

print b

print a
