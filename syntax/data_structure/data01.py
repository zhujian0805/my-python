#!/usr/bin/python
import urllib, re
from pprint import pprint

res = urllib.urlopen("http://config-vip/directory/locations/hostname")

locations = {}
location = None
interface = None
address = None

for line in res.readlines():
    matchObj = re.search(r'location: "(.*)"', line)
    if matchObj:
        location = matchObj.group(1)
        locations[location] = {}
    matchObj = re.search(r'name: "(.*)"', line)
    if matchObj:
        interface = matchObj.group(1)
        locations[location][interface] = ''
    matchObj = re.search(r'address: "(.*)"', line)
    if matchObj:
        address = matchObj.group(1)
        locations[location][interface] = address

pprint(locations)
