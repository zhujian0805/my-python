#!/usr/bin/python

import re


def strConv(s):
    s = str(s)
    while True:
        (s, count) = re.subn(r"(\d)(\d{3})((:?,\d\d\d)*)$", r"\1,\2\3", s)
        if count == 0: break
    return s


print strConv(12345)
