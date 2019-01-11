#!/usr/bin/env python
from pexpect import pxssh
import pexpect
import getpass
import sys
import os

hostname = sys.argv[1]

if os.environ.has_key("USERNAME"):
    username = os.environ["USERNAME"]
else:
    username = os.environ["USER"]

password = os.environ["LDAPUSERPW"]
command = " ".join(sys.argv[2:])

s = pexpect.spawn("ssh -q -o StrictHostKeyChecking=no %s@%s" % (username, hostname))
s.expect(".*password.*")
s.sendline(password)
s.expect(".*")
s.sendline('sudo su -')
s.expect(".*password.*for.*")
s.sendline(password)
s.expect(".*#")
print("******** Running command: %s on: %s ********" % (command, hostname))
print("------------------------------------------------------------------------")
s.sendline(command)
s.logfile = sys.stdout
s.expect(".*#")
print("\n")
