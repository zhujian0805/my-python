#!/usr/bin/python
#from functools import wraps
import functools

"""
Adding the link for the excellent explaination for decorator

http://thecodeship.com/patterns/guide-to-python-function-decorators/

"""

class Tester(object):
    """tester class"""
    def __init__(self):
        pass

    def say(self, tag):
        def decorator(f):
            @functools.wraps(f)   #Functools to the rescue
            def wrapper(*args, **kwargs):
                print "Hello %s" % tag
                f(args[0])
            return wrapper
        return decorator

def make_default_app_wrapper(name):
    ''' Return a callable that relays calls to the current default app. '''
    @functools.wraps(getattr(Tester, name))
    def wrapper(*a, **ka):
        return getattr(tester, name)(*a, **ka)
    return wrapper


tester = Tester()
shortcut = make_default_app_wrapper("say")

@shortcut('James Zhu')
def sayhi(it):
    print "hello %s" % it

sayhi("Nemo")
