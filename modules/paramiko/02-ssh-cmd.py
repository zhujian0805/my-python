#!/usr/bin/python
import getpass
import os
import paramiko
import socket
import sys
import pexpect
import re

client = paramiko.client.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
try:
    #client.connect(sys.argv[1], port=22, username='username', password='passwd')
    client.connect(
        sys.argv[1], port=22, username='jameszhu', password='VFR$bgt5nhy6')
except:
    try:
        client.connect(
            sys.argv[1], port=22, username='username', password='passwd')
    except:
        print "something wrong while connecting to %s!" % "AMM"
        sys.exit(5)

try:
    stdin, stdout, stderr = client.exec_command('sleep 4000')
except SSHException:
    print "something wrong while executing command %s on %s!"
    sys.exit(6)

for line in stdout.readlines():
    print line.strip()
