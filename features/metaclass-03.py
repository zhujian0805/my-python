#!/usr/bin/python

from functools import wraps
import time

def logged(time_format, name_prefix=""):
    def decorator(func):
        if hasattr(func, '_logged_decorator') and func._logged_decorator:
            return func
 
        @wraps(func)
        def decorated_func(*args, **kwargs):
            start_time = time.time()
            print "- Running '%s' on %s " % (
                                            name_prefix + func.__name__,
                                            time.strftime(time_format)
                                 )
            result = func(*args, **kwargs)
            end_time = time.time()
            print "- Finished '%s', execution time = %0.3fs " % (
                                            name_prefix + func.__name__,
                                            end_time - start_time
                                 )
 
            return result
        decorated_func._logged_decorator = True
        return decorated_func
    return decorator


def log_everything_metaclass(class_name, parents, attributes):
    print "Creating class", class_name
    myattributes = {}
    for name, attr in attributes.items():
        myattributes[name] = attr
        if hasattr(attr, '__call__'):
            myattributes[name] = logged("%b %d %Y - %H:%M:%S", class_name + ".")(attr)
    return type(class_name, parents, myattributes)
 
class C(object):
    __metaclass__ = log_everything_metaclass
 
    def __init__(self, x):
        self.x = x
 
    def print_x(self):
        print self.x
 
# Usage:
print "Starting object creation"
c = C("Test")
c.print_x()
