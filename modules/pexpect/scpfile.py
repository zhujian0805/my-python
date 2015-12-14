#!/usr/bin/python

import sys
import pexpect
import time

mypassword = 'VFR$bgt5nhy6'

child = pexpect.spawn('scp /etc/passwd jameszhu@localhost:/tmp')
#child.logfile = sys.stdout
child.expect('assword:')
child.sendline(mypassword)
child.expect(pexpect.EOF)
child.close()
