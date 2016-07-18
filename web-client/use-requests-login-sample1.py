#!/usr/bin/python
import requests
from pprint import pprint
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

s = requests.Session()

payload = {'email': 'zhujian0805@gmail.com', 'password': 'zhujian'}
url = 'http://passport.renren.com/PLogin.do'

s.post(url, payload)

#now access protected page: http://www.renren.com/702740495/profile
protected_url = 'http://www.renren.com/702740495/profile'

res = s.get(protected_url)

print res.text
