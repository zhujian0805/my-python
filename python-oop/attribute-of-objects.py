#!/usr/bin/python
# coding=utf-8
""" This is for pylint """
# ===============================================================================
#
#         FILE: test.py
#
#        USAGE: ./test.py
#
#  DESCRIPTION:
#
#      OPTIONS: ---
# REQUIREMENTS: ---
#         BUGS: ---
#        NOTES: ---
#       AUTHOR: James Zhu (), zhujian0805@gmail.com
# ORGANIZATION: ZJ
#      VERSION: 1.0
#      CREATED: Tue 06 Jun 2017 05:32:16 PM CST
#     REVISION: ---
# ===============================================================================

import sys


class FuckYou(object):
    """ Pylint """
    def __init__(self):
        """ pylint """
        self.fuck = "YES"

    def testing(self):
        """ pylint """
        print self.fuck

    def test01(self):
        """ pylint """
        print self.fuck


if __name__ == "__main__":
    print "yes"
    print "all attributes of __main__"
    print "-----------------------------------------------------"
    print dir(sys.modules["__main__"])
    print "all attributes of belonging object FuckYou's attributes"
    print "-----------------------------------------------------"
    print dir(getattr(sys.modules["__main__"], "FuckYou"))
