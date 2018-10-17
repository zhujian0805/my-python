#!/usr/bin/python
"""
DocString
"""

#import json
from pprint import pprint as pp
import maxminddb

ips = open('ip.txt').readlines()

reader = maxminddb.open_database(
    '/home/jzhu/venv/lib/python2.7/site-packages/_geoip_geolite2/GeoLite2-City.mmdb'
)

for ip in ips:
    ret = reader.get(ip.strip())
    if ret is not None:
        #pp(ret)
        if ret.has_key('city') and ret['country']['iso_code'] == 'CN':
            if ret['city']['names'].has_key('zh-CN'):
                print(ret['city']['names']['zh-CN'])
            else:
                print(ret['city']['names']['en'])
        elif ret.has_key(
                'subdivisions') and ret['country']['iso_code'] == 'CN':
            print ret['subdivisions'][0]['names']['zh-CN']
