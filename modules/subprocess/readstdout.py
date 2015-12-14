#!/usr/bin/python

import subprocess

proc = subprocess.Popen("ls -ltr /tmp/", stdout=subprocess.PIPE, shell=True)
(output, error) = proc.communicate()

for line in output.splitlines():
    print line
