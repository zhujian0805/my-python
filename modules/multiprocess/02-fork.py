#!/usr/bin/python
import os, errno
import sys, time

pid = os.fork()


def PidIsAlive(pid):
    try:
        return os.waitpid(pid, os.WNOHANG) == (0, 0)
    except OSError, e:
        if e.errno != errno.ECHILD:
            raise


if pid == 0:
    #time.sleep(10)
    pass
else:
    if PidIsAlive(pid):
        print "%s gone" % pid
    else:
        print "%s still running" % pid

    time.sleep(100)
