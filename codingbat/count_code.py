#!/usr/bin/python


def count_code(str):
    count = 0
    for i in xrange(0, len(str) - 3):
        s = str[i:i + 4]
        if s == 'code' or (s[:2] == 'co' and s[3:] == 'e'):
            count = count + 1
    return count


print count_code("aaacope")
