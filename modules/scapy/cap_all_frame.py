#!/usr/bin/python

from scapy.all import *
import sys


def pkt_callback(pkt):
    pkt.show()    # debug statement


sniff(iface=sys.argv[1], prn=pkt_callback, filter="ip", store=0)
