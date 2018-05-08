#!/usr/bin/env python
# coding=utf-8
#===============================================================================
#
#         FILE: test-scope02.py
#
#        USAGE: ./test-scope02.py
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
#      CREATED: Tue 08 May 2018 08:44:49 PM CST
#     REVISION: ---
#===============================================================================

ttt = ''
aaa = []

def setit(it):
    global ttt
    ttt = it
    aaa.append(it)

def showit():
    global ttt
    print(ttt)
    print(aaa)

