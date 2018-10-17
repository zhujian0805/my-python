#!/usr/bin/python
#coding=utf-8
import urllib2
url = "http://xxx"    #需要访问的URL
try:
    response = urllib2.urlopen(url)
except urllib2.URLError, e:
    if hasattr(e, "reason"):
        print "Failed to reach the server"
        print "The reason:", e.reason
    elif hasattr(e, "code"):
        print "The server couldn't fulfill the request"
        print "Error code:", e.code
        print "Return content:", e.read()
else:
    pass    #其他异常的处理
