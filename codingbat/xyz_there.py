#!/usr/bin/python
import sys


def xyz_there(str):
    count = 0
    if len(str) < 3:
        return False
    for i in xrange(0, len(str) - 2):
        s = str[i:i + 3]
        #        print s
        if s == 'xyz':
            if i == 0:
                return True
            else:
                if str[i - 1] != '.':
                    return True
                else:
                    pass
        else:
            pass
    return False


print xyz_there(sys.argv[1])
