#!/usr/bin/env python
# coding=utf-8
# ===============================================================================
#
#         FILE: connect_string_examples.py
#
#        USAGE: ./connect_string_examples.py
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
#      CREATED: Fri 18 Jan 2019 11:17:36 PM CST
#     REVISION: ---
# ===============================================================================

a, b = 'hello', 'world'

# 1
print(a + b)

# 2
print(a, b)

# 3
print('hello'    'world')

# 4
print('hello''world')

# 5
print("%s %s" % ('hello', 'world'))

# 6
print('{} {}'.format('hello', 'world'))

# 7
print('-'.join(['hello', 'world']))

# 8
print(f'{a} {b}')
