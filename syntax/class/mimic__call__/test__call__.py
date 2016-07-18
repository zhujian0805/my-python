#!/usr/bin/python

class Callee:
    def __call__(self, *pargs, **kargs):
        print('Called:', pargs, kargs)

C = Callee()

C(1,2,3)
