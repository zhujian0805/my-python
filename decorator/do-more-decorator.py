#!/usr/bin/python

from functools import wraps

"""
Adding the link for the excellent explaination for decorator

http://thecodeship.com/patterns/guide-to-python-function-decorators/

"""

def target():
    def decorator(f):
        @wraps(f)   #Functools to the rescue
        def wrapper(*args, **kwargs):
            print args[0] + " " + kwargs['name']
        return wrapper
    return decorator



@target()
def prtsomething(something, name="James Zhu"):
    """returns some text"""
#    pass


prtsomething("I L U", name="Yili")
prtsomething("I L U", name="Nemo")
