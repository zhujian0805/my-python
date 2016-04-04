#!/usr/bin/python

import sys

class_name = sys.argv[1]

print "Class name is %s" % class_name

class ABC():
    def __init__(self):
        print "This is class ABC"

if __name__ == "__main__":
    myclass = getattr(sys.modules[__name__], class_name)
    print("instantiate the class %s" % class_name)
    myobj = myclass()
