#!/usr/bin/env python
# coding=utf-8
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
    def __init__(self):
        pass

    def testing(self):
        pass


if __name__ == "__main__":
    print("yes")
    print("all attributes of __main__")
    print("-----------------------------------------------------")
    print(dir(sys.modules["__main__"]))
    print("all attributes of belonging object FuckYou's attributes")
    print("-----------------------------------------------------")
    print(dir(getattr(sys.modules["__main__"], "FuckYou")))
