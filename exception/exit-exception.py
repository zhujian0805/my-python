#!/usr/bin/python
import sys

#  exit actually raise an exception SystemExit, So be careful when using in try/except
#  clause
#
#
try:
    sys.exit(1)
except SystemExit as ex:
    template = "An exception of type {0} occured. Arguments:\n{1!r}"
    message = template.format(type(ex).__name__, ex.args)
    print message
