#!/usr/bin/python

import types
from pprint import pprint

def create_function(name, args):

    def y():
      print "create function...."

    y_code = types.CodeType(args, \
                y.func_code.co_nlocals, \
                y.func_code.co_stacksize, \
                y.func_code.co_flags, \
                y.func_code.co_code, \
                y.func_code.co_consts, \
                y.func_code.co_names, \
                y.func_code.co_varnames, \
                y.func_code.co_filename, \
                name, \
                y.func_code.co_firstlineno, \
                y.func_code.co_lnotab)

    return types.FunctionType(y_code, y.func_globals, name)

myfunc = create_function('myfunc', 3)

print repr(myfunc)
print myfunc.func_name
print myfunc.func_code.co_argcount

print myfunc(1,2,3)
#myfunc(1,2,3,4)
# TypeError: myfunc() takes exactly 3 arguments (4 given)
