#!/usr/bin/python
from pprint import pprint


class Test:
    class TestInTest:
        def __init__(self, v1, v2):
            self.v1 = v1
            self.v2 = v2

        def showvar(self):
            print self.v1
            print self.v2

    def sayhi(self):
        print "Hello, Iam Instance of Test Class"


test1 = Test()

tInT = test1.TestInTest(1, 2)

tInT.showvar()

test1.sayhi()
