#!/usr/bin/python

from functools import wraps
"""
Adding the link for the excellent explaination for decorator

http://thecodeship.com/patterns/guide-to-python-function-decorators/

"""


def target(tag):
    def decorator(f):
        @wraps(f)    #Functools to the rescue
        def wrapper(*args, **kwargs):
            return "Hello %s: \n%s" % (tag, f(args[0]))

        return wrapper

    return decorator


@target("Visitors")
def prtsomething(something):
    """returns some text"""
    return something


print prtsomething("Welcome to my workspace")

print prtsomething.__name__
print prtsomething.__doc__
print prtsomething.__module__
