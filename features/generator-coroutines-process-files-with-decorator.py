#!/usr/bin/python
import os, sys
import fnmatch

def coroutine(func):
  def start(*args,**kwargs):
    g = func(*args,**kwargs)
    g.next()
    return g
  return start

@coroutine
def find_files(target):
  while True:
    topdir, pattern = (yield)
    for path, dirname, filelist in os.walk(topdir):
      for name in filelist:
        if fnmatch.fnmatch(name, pattern):
          target.send(os.path.join(path,name))

import gzip, bz2
@coroutine
def opener(target):
  while True:
    name = (yield)
    if name.endswith(".gz"): f = gzip.open(name)
    elif name.endswith(".bz2"): f = bz2.BZ2File(name)
    else: f = open(name)
    target.send(f)

@coroutine
def cat(target):
  while True:
    f = (yield)
    for line in f:
      target.send(line)

@coroutine
def grep(pattern, target):
  while True:
    line = (yield)
    if pattern in line:
      target.send(line)

@coroutine
def printer():
  while True:
    line = (yield)
    sys.stdout.write(line)


finder = find_files(opener(cat(grep("mpm", printer()))))

# Now, send a value
finder.send(("/var/log/apache2","error.log*"))
