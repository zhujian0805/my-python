#!/usr/bin/python

def mymetaclass(name, parents, attributes):
  return "Hello"

class C(object):
  __metaclass__ = mymetaclass

print C

print type(C)
