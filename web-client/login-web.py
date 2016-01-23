#!/usr/bin/python

import urllib2
import urllib
import sys
from cookielib import CookieJar

cj = CookieJar()

url = 'http://passport.renren.com/PLogin.do'
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

values = {'email': 'zhujian0805@gmail.com', 'password': 'zhujian***'}
data = urllib.urlencode(values)
try:
    response = opener.open(url, data)
#print response.read()
except:
    print "Error"
    sys.exit(1)

print type(response)
print dir(response)
print response.code

print "now you can access your protected contents"
#response2 = opener.open('http://blog.renren.com/blog/702740495/932392877?myblog')
#response2 = opener.open('http://www.renren.com/702740495/profile')
#print response2.read()
