#!/usr/bin/python
import hashlib
import re
import sys
import getopt


def crack(a1, a2, b1, b2, pattern):
    for i in xrange(a1, a2):
        for j in xrange(b1, b2):
            string = str(i) + '-' + str(j)
            m = hashlib.md5()
            m.update(string)
            result = m.hexdigest()
            print "%s --> %s" % (string, result)
            if re.match(pattern, result, re.I):
                exit(0)


def usage():
    print "Wrong use!!!!!"


if __name__ == "__main__":
    fstr = sstr = opts = []
    pattern = args = ''

    if (len(sys.argv) != 7):
        usage()
        sys.exit(2)

    try:
        opts, args = getopt.getopt(sys.argv[1:], "f:s:p:",
                                   ["firstrange=", "secondrange="])
    except getopt.GetoptError as err:
        # print help information and exit:
        print str(
            err)    # will print something like "option -a not recognized"
        usage()
        sys.exit(2)

    for o, a in opts:
        if o in ('-f', "--firstrange"):
            fstr = a.split("-")
        elif o in ('-s', "--secondrange"):
            sstr = a.split("-")
        elif o in ("-p"):
            pattern = a
        else:
            assert False, "unhandled option"

    crack(int(fstr[0]), int(fstr[1]), int(sstr[0]), int(sstr[1]), pattern)
