#!/usr/bin/python

import copy

a = [1, 2, [12, 32], 3]

b = copy.deepcopy(a)

b[2][0] = 10101010

print a
print b
