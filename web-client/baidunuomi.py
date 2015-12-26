#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys, urllib, urllib2, json
from pprint import pprint

url = 'http://apis.baidu.com/baidunuomi/openapi/shopdeals?shop_id=1745896'

# Set default encoding here, now your can process utf8 characters with in the python code
import sys  
reload(sys)  
sys.setdefaultencoding('utf8')   


req = urllib2.Request(url)

req.add_header("apikey", sys.argv[1])

resp = urllib2.urlopen(req)
content = resp.read()
if(content):
    for deal in json.loads(content)['deals']:
        for key in deal.keys():
            if key == 'title':
                print key, deal[key]
