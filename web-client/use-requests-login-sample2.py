#!/usr/bin/python
import requests
from pprint import pprint
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

payload = {'email': 'zhujian0805@gmail.com', 'password': 'zhujian'}
url = 'http://passport.renren.com/PLogin.do';
protected_url = 'http://www.renren.com/702740495/profile'

#now access protected page: http://www.renren.com/702740495/profile
with requests.Session() as s:
    s.post(url, data=payload)
    
    # print the html returned or something more intelligent to see if it's a
    # successful login page.
    #print s.text

    # An authorised request.
    r = s.get(protected_url)
    print r.text
