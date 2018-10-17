#!/usr/bin/python
import os
import sys, time

pid = os.fork()

if pid == 0:
    pass
    #time.sleep(3)
else:
    #print os.waitpid(pid, os.WIFSTOPPED)
    #print os.waitpid(pid, os.WCONTINUED)
    #print os.waitpid(pid, os.WNOHANG)
    pid, status = os.waitpid(pid, os.WUNTRACED | os.WNOHANG)
    print pid
    print status
    while True:
        if os.WIFSTOPPED(pid):
            wait()
            break
    print "end waiting"
    time.sleep(20)
