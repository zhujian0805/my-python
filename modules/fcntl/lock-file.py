#!/usr/bin/python
import fcntl, time, os

fh = open("/tmp/test.log", "a")

fcntl.flock(fh, fcntl.LOCK_EX)
print "lock done"
fh.write(str(os.getpid()) + "\n")
time.sleep(5)
fcntl.flock(fh, fcntl.LOCK_UN)
print "unlock done"
fh.close()
