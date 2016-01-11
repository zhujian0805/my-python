#!/usr/bin/python
#coding=utf-8
import urllib2
url="xxxxxx"  #需要访问的URL
try:
    response=urllib2.urlopen(url)
except urllib2.HTTPError,e:    #HTTPError必须排在URLError的前面
    print "The server couldn't fulfill the request"
    print "Error code:",e.code
    print "Return content:",e.read()
except urllib2.URLError,e:
    print "Failed to reach the server"
    print "The reason:",e.reason
else:
    #something you should do
    pass  #其他异常的处理
