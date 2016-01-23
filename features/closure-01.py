#!/usr/bin/python

# http://www.shutupandship.com/2012/01/python-closures-explained.html
# http://www.programiz.com/python-programming/closure
# http://ynniv.com/blog/2007/08/closures-in-python.html


def outer(o):
    """Outer function"""

    def inner(i):
        """Inner function"""
        print "%s, %s" % (o, i)

    return inner


closure_func = outer("Fuck")

closure_func("You")
