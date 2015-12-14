#!/usr/bin/python

li = ['abs', 'asdfsf', 2323]

print li

for i in li:
  print "item {} in li".format(i)

for i in repr(li):
  print "item {} in repr(li)".format(i)

for i in eval(repr(li)):
  print "item {} in eval(repr(li))".format(i)
