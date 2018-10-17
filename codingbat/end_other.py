#!/usr/bin/python


def end_other(a, b):
    la = len(a)
    lb = len(b)
    a = a.lower()
    b = b.lower()
    if la > lb:
        return (b == a[la - lb:])
    else:
        return (a == b[lb - la:])


print end_other('abc', 'hiabc')
