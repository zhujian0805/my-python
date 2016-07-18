#!/usr/bin/python

dict = {'Disk': '1234', 'Alice': '2341', 'Beth': '9102', 'Cecil': '3258'}

skeys = dict.keys()

skeys.sort()

for key in skeys:
    print key, dict[key], "\n"
