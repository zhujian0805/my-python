#!/usr/bin/python

# Example-36.py
from __future__ import print_function
import sys
import libvirt
from xml.dom import minidom
from pprint import pprint as pp

conn = libvirt.open('qemu:///system')
if conn == None:
    print('Failed to open connection to qemu:///system', file=sys.stderr)
    exit(1)

dom = conn.lookupByName('instance-00029ff0')
if dom == None:
    print('Failed to find the domain ' + domName, file=sys.stderr)
    exit(1)

raw_xml = dom.XMLDesc(0)

print(raw_xml)

xml = minidom.parseString(raw_xml)
domainTypes = xml.getElementsByTagName('nova:name')

print(dir(domainTypes))

conn.close()
exit(0)
