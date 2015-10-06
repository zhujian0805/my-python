#!/usr/bin/python

def deco_try(func): 
    def _decotry(*arg, **kwarg): 
        try: 
            func(*arg, **kwarg) 
        except Exception, ex: 
            print 'app error', str(ex) 
            raise ex 
    return _decotry


@deco_try
def read(file):
    x = open(file, 'r')
    line = x.readline()
    while True:
      if line:
        print line
      else:
        break
      line = x.readline()

read('/tmp/abc')
