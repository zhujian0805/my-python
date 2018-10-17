#!/usr/bin/python
from optparse import OptionParser
import getpass
import os
import sys
from threading import Thread
import ConfigParser
import ldap
from pprint import pprint
import re
import cgi, cgitb


def readLoctions(path):
    fh = open(path)
    lines = {}
    while True:
        line = fh.readline().strip()
        print line
        if line:
            cols = line.split()
            lines[cols[0]] = {}
            lines[cols[0]]['location'] = cols[0]
            lines[cols[0]]['slot'] = cols[1]
        else:
            break
    return lines


if __name__ == "__main__":
    lines = readLoctions("/tmp/cn1.txt")
    print lines
