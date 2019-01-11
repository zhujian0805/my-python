#!/usr/bin/env python
from pexpect import pxssh
import getpass
import sys
import os

hostname = sys.argv[1]
username = os.environ["USERNAME"]
password = os.environ["MYPASSWORD"]
command = " ".join(sys.argv[2:])

try:
    s = pxssh.pxssh(options={ "StrictHostKeyChecking": "no", "UserKnownHostsFile": "/dev/null"})
    s.login(hostname, username, password)
    s.sendline(command)
    s.prompt()
    print(s.before)
    s.logout()
except pxssh.ExceptionPxssh as e:
    print("pxssh failed on login.")
    print(e)
