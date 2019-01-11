#!/usr/bin/env python
from pexpect import pxssh
import pexpect
import getpass
import sys
import os

hostname = sys.argv[1]
username = os.environ["USERNAME"]
password = os.environ["MYPASSWORD"]
command = " ".join(sys.argv[2:])

s = pexpect.spawn("ssh -q -o StrictHostKeyChecking=no %s@%s" % (username, hostname))
s.expect(".*password.*")
s.sendline(password)
s.expect(".*")
s.sendline('sudo su -')
s.expect(".*password.*for.*")
s.sendline(password)
s.expect(".*#")
s.sendline(command)
s.logfile = sys.stdout
s.expect(".*#")
print
