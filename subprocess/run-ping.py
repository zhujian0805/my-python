#!/usr/bin/python

import subprocess
import sys
import time

cmd = [ "/bin/ping", "-c4", "-W2", 'hostname' ];
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


time.sleep(1200)
