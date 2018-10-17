#!/usr/bin/python

import subprocess
import sys

#cmd = [ '/bin/ls', '/tmp' ]
cmd = ['top', '-n 1']
#cmd = '/bin/ls'
#cmd = 'ps -ef'

try:
    #proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
except Exception as e:
    print e
    sys.exit(2)

for line in proc.communicate()[0].splitlines():
    #for line in proc.communicate()[0]:
    print line
