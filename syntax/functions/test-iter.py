#!/usr/bin/env python
import copy


class Deleteit:
    def __init__(self, p1):
        self.p = p1

    def delit(self):
        aa = self.p[0]
        self.p.remove(aa)
        return aa

    def prtit(self):
        print self.p


arr = [1, 2, 3, 4, 5, 6, 7, 8, 9]
abc = Deleteit(arr)

for i in iter(abc.delit, 4):
    print i
