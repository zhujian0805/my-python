#!/usr/bin/env python
""" This is for running COMMAND remotely"""
import sys
import os
import time
import argparse
import pexpect
from multiprocessing import Process, Queue


class ExpectMe():
    """ expect me"""

    def __init__(self, username, password, hostname):
        """ initialization """
        self.hostname = hostname
        self.username = username
        self.password = password
        self.ignore = False
        try:
            self.s = pexpect.spawn("ssh -q -o StrictHostKeyChecking=no %s@%s" % (self.username, self.hostname), timeout=3)
            self.s.setwinsize(65535, 65535)
            self.login()
        except pexpect.exceptions.TIMEOUT or pexpect.exceptions.EOF:
            self.ignore = True

    def login(self):
        """ login """
        self.s.expect(".*password.*")
        self.s.sendline(self.password)
        self.s.expect(".*")
        self.s.sendline('sudo su -')
        self.s.expect(".*password.*for.*")
        self.s.sendline(self.password)
        self.s.expect(".*#")

    def RunCmd(self, command="uptime"):
        """ run command """
        if self.ignore:
            print "******************************************************************************************"
            print "This server(%s) is not reachable, ignore for now and please check!" % self.hostname
            print "******************************************************************************************"
            return
        print("******** Running COMMAND: %s on: %s ********" % (command, self.hostname))
        print("-------------------------------------------------------------------------------------------------------------------------------------------")
        self.s.sendline(command)
        self.s.logfile = sys.stdout
        self.s.expect(".*#")
        print("\n")


def parse_opts():
    parser = argparse.ArgumentParser(description='Run commands remotely', formatter_class=lambda prog: argparse.HelpFormatter(prog, max_help_position=35, width=130))
    required_group = parser.add_argument_group('Required parameters')
    required_group.add_argument('-h', '--hosts', dest='hosts', default="",
                                required=True, help='specify host to be managed')


def worker(tasks, USER, PASSWD):
    for host in iter(tasks.get, 'STOP'):
        EXP = ExpectMe(USER, PASSWD, host)
        EXP.RunCmd(COMMAND)

if __name__ == '__main__':

    processes = []
    NUMBER_OF_PROCESSES = 1

    HOST = sys.argv[1]
    if os.environ.has_key("USERNAME"):
        USER = os.environ["USERNAME"]
    else:
        USER = os.environ["USER"]

    PASSWD = os.environ["LDAPUSERPW"]
    COMMAND = " ".join(sys.argv[2:])
    if not COMMAND:
        COMMAND = 'echo;cat /etc/redhat-release; echo; uptime;echo;route -n;echo;df;echo'

    tasks = Queue()
    for host in HOST.split(','):
        tasks.put(host)

    for i in range(NUMBER_OF_PROCESSES):
        p = Process(target=worker, args=(tasks, USER, PASSWD)).start()
        processes.append(p)

    while not tasks.empty():
        time.sleep(1)

    for i in range(NUMBER_OF_PROCESSES):
        tasks.put('STOP')


