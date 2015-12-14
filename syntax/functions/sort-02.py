#!/usr/bin/python
import re

def ccc(x, y):
  if re.search(r'[a-zA-Z]', str(x)):
    return 0
  elif re.search(r'[a-zA-Z]', str(y)):
    return 0
  if int(x) >= int(y):
    return 1
  else:
    return -1

l = [3,4,6,1,3,2,5,7,5,43,5,6,3]
l.sort(ccc)

print l
