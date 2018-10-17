#!/usr/bin/env python
# coding=utf-8
#===============================================================================
#
#         FILE: scope.py
#
#        USAGE: ./scope.py
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
#      CREATED: Tue 08 May 2018 08:33:20 PM CST
#     REVISION: ---
#===============================================================================

foo = 'MODULE level string'


def aaa():
    foo = "first level in FUNC aaaa"
    print(foo)

    def bbb():
        foo = "Second level in FUNC bbbb"
        print(foo)

    def ccc():
        print(foo)

    bbb()
    ccc()


aaa()
