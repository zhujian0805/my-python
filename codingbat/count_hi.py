#!/usr/bin/python


def count_hi(str):
    count = 0
    for i in xrange(0, len(str) - 1):
        s = str[i:i + 2]
        if s == 'hi':
            count = count + 1
    return count


print count_hi('hasdjhilsfhi')
