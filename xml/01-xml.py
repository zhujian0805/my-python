#!/usr/bin/python
import xml.etree.ElementTree as ET

xmlstr = """<?xml version="1.0"?>
<clustat version="4.1.1">
  <cluster name="test_host" id="53968" generation="108"/>
  <quorum quorate="1" groupmember="1"/>
  <nodes>
    <node name="test-admin-host01" state="1" local="1" estranged="0" rgmanager="1" rgmanager_master="0" qdisk="0" nodeid="0x00000001"/>
    <node name="test-admin-host02" state="1" local="0" estranged="0" rgmanager="1" rgmanager_master="0" qdisk="0" nodeid="0x00000002"/>
  </nodes>
  <groups>
    <group name="service:host" state="112" state_str="started" flags="0" flags_str="" owner="test-admin-host01" last_owner="test-admin-host02" restarts="0" last_transition="1423109827" last_transition_str="Thu Feb  5 04:17:07 2015"/>
  </groups>
</clustat>
"""

root = ET.fromstring(xmlstr)

for child in root.iter():
    print child.tag
    if child.tag == 'node':
        print child.attrib['name']
