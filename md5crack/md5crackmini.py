#!/usr/bin/python
import hashlib
import re
import sys
import getopt


def crack(pattern):
    for i in xrange(1, 999):
        for j in xrange(1, 9999):
            string = str(i) + '-' + str(j)
            m = hashlib.md5()
            m.update(string)
            result = m.hexdigest()
            print "%s --> %s" % (string, result)
            if re.match(pattern, result, re.I):
                exit(0)


if __name__ == "__main__":
    crack(sys.argv[1])
