#!/usr/bin/python
import getpass
import os
import paramiko
import socket
import sys
import pexpect
import re
import threading

class Enclosure:
    """This is a class for manipulate enclosure"""
    def __init__(self, mmname):
        self.mm0 = mmname + '-mm0' + '.sample.net'
        self.mm1 = mmname + '-mm1' + '.sample.net'
        self.mm = mmname

    def connect(self):
        self.client = paramiko.client.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            self.client.connect(self.mm0, port=22, username='username', password='passwd', timeout=10)
        except:
            try:
                self.client.connect(self.mm1, port=22, username='username', password='passwd', timeout=10)
            except:
                print "something wrong while connecting to %s!" % self.mm0
                return
        return self.client

    def isItHP(self):
        hp = 0
        self.manufacturer = 'IBM'

        stdin, stdout, stderr = self.execCmd('show oa info')
        for line in stdout.readlines():
            if re.search(r'Manufacturer  : HP', line):
                hp = 1
                break
        
        if hp:
            self.manufacturer = 'HP'
        else:
            self.manufacturer = 'IBM'
        return hp

    def execCmd(self, cmd):
        try:
            return self.client.exec_command(cmd, timeout=20)
        except:
            print "something wrong while executing command %s on %s" % (cmd, self.mm)
            return

    def showSyslog(self, entity):
        stdin, stdout, stderr = self.execCmd('show syslog %s' % entity)
        for line in stdout.readlines():
            print line.strip()

    def showBladeStatus(self, blade):
        stdin, stdout, stderr = self.execCmd('show server status %s' % blade)
        for line in stdout.readlines():
            print line.strip()

    def showBladeinfo(self, blade):
        stdin, stdout, stderr = self.execCmd('show server info %s' % blade)
        for line in stdout.readlines():
            print line.strip()

if __name__ == "__main__":
    amm = Enclosure(sys.argv[1])
    if not amm.connect():
        sys.exit(1)
    amm.showBladeinfo(1)
    amm.showBladeStatus(1)
    amm.showSyslog("server 1")
    print "Ending"
