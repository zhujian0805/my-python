#!/usr/bin/python


class Test:
    def __init__(self, v1, v2):
        self.v1 = v1
        self.v2 = v2

    def __str__(self):
        return "Test (%d, %d) " % (self.v1, self.v2)

    def __add__(self, other):
        return Test(self.v1 + other.v1, self.v2 + other.v2)


a = Test(1, 2)
b = Test(2, 3)

print a + b
