#!/usr/bin/env python

import os
import sys
import time

class Logwatcher():

    def __init__(self, filename):
        self.filename = filename
        self.lastpos = 0
        fileobj = open(self.filename, "r")
        while(1):
            line = fileobj.readline()
            if not line:
                break
            print line.strip()
        self.lastpos = fileobj.tell()
        fileobj.close()


    def readlines(self):
        fileobj = open(self.filename, "r")
        fileobj.seek(self.lastpos)
        while(1):
            line = fileobj.readline()
            if not line:
                break
            print line.strip()
        self.lastpos = fileobj.tell()

    def loop(self):
        while(1):
            self.readlines()
            time.sleep(0.001)
            


logwatcher = Logwatcher("abc.log")

logwatcher.loop()
