#!/usr/bin/python

# Seems python version before 2.4 doesn't support this syntax below
# It works and tested on 2.7

import sys
import subprocess
import os.path

cmd1 = '/bin/echo show paths'
cmd2 = 'grepp path'
cmd1 = cmd1.split()
cmd2 = cmd2.split()
try:
    p1 = subprocess.Popen(cmd1, stdout=subprocess.PIPE)
    p2 = subprocess.Popen(
        cmd2, stdin=p1.stdout, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    #print p2.communicate()
    (output, errors) = p2.communicate()
    print p2.returncode
except Exception as ex:
    # in python 2.4/2.5, you should use the syntax as below line, chaning the "as" to ","
    #except Exception , ex:
    template = "An exception of type {0} occured. Arguments:\n{1!r}"
    message = template.format(type(ex).__name__, ex.args)
    print message
