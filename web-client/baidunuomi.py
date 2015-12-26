#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys, urllib, urllib2, json
from pprint import pprint

url = 'http://apis.baidu.com/baidunuomi/openapi/shopdeals?shop_id=1745896'


req = urllib2.Request(url)

req.add_header("apikey", sys.argv[1])

resp = urllib2.urlopen(req)
content = resp.read()
if(content):
    pprint(content)
