#!/usr/bin/python
import sys
from pprint import pprint

fh = open("/etc/fstab")

lines = (t.strip() for t in fh)

comments = (t for t in lines if t[0] == '#')

for c in comments:
    print c
