#!/usr/bin/env python
""" This is for running COMMAND remotely"""
import sys
import os
import argparse
import pexpect


class ExpectMe():
    """ expect me"""

    def __init__(self, username, password, hostname):
        """ initialization """
        self.hostname = hostname
        self.username = username
        self.password = password
        self.s = pexpect.spawn("ssh -q -o StrictHostKeyChecking=no %s@%s" % (self.username, self.hostname))
        self.s.setwinsize(65535, 65535)
        self.login()

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
        print("******** Running COMMAND: %s on: %s ********" % (command, self.hostname))
        print("---------------------------------------------------------------")
        self.s.sendline(command)
        self.s.logfile = sys.stdout
        self.s.expect(".*#")
        print("\n")


def parse_opts():
    parser = argparse.ArgumentParser(description='Run commands remotely', formatter_class=lambda prog: argparse.HelpFormatter(prog, max_help_position=35, width=130))
    required_group = parser.add_argument_group('Required parameters')
    required_group.add_argument('-h', '--hosts', dest='hosts', default="",
                                required=True, help='specify host to be managed')


if __name__ == '__main__':

    HOST = sys.argv[1]
    if os.environ.has_key("USERNAME"):
        USER = os.environ["USERNAME"]
    else:
        USER = os.environ["USER"]

    PASSWD = os.environ["LDAPUSERPW"]
    COMMAND = " ".join(sys.argv[2:])
    if not COMMAND:
        COMMAND = 'echo;uptime;echo;route -n;echo;df;echo'

    for host in HOST.split(','):
        EXP = ExpectMe(USER, PASSWD, host)
        EXP.RunCmd(COMMAND)


