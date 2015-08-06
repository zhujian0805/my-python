#!/usr/bin/python
import sys
from pprint import pprint

a = xrange(10)

b = ( 10*i for i in a )

i = 0;
while i < 10:
  print b.next();
  i += 1
