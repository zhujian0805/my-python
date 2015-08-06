#!/usr/bin/python
from optparse import OptionParser
import getpass
import os
import sys
from threading import Thread
import ConfigParser
import ldap
from pprint import pprint
import re
import cgi, cgitb


def hashhosts(pl):
	hashhost = {}
	pl = pl.lower()
	try:
		matchobj = re.match(r'(.*=?)r.*(\d{1,})e(\d{1,})b(\d{1,})', pl, re.M|re.I)
	except:
		return
		
	parent = matchobj.group(1) + "-rack0" + matchobj.group(2) + "-enclosure0" + matchobj.group(3)
	pp = matchobj.group(1) + 'r' + matchobj.group(2) + 'e' + matchobj.group(3)
	section = "slot %s" % matchobj.group(4)
	if(hashhost.has_key(parent)):
		hashhost[parent]['section'].append(section)
	else:
		hashhost[parent] = {}
		hashhost[parent]['section'] = []
		hashhost[parent]['name'] = pp.upper()
		hashhost[parent]['section'].append(section)
	return hashhost

def strinlist(s, l):
	p = re.compile(r'.*%s$' % s)
	for i in l:
		#if s in i:
		if(re.match(p,i,re.M|re.I)):
			return(True)	
	return False

def print_header():
	print('<head>')
	print('<meta charset="utf-8">')
	print('<meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">')
	print('<title>Searching your blade</title>')
	print('<link rel="stylesheet" href="css/style.css">')
	print('<!--[if lt IE 9]><script src="//html5shim.googlecode.com/svn/trunk/html5.js"></script><![endif]-->')
	print('</head>')


def prtinfo(attrlist, searchfor):
#	if searchtype == "macaddr":
#		attrlist = devinfo(ldapobj, searchfor, type=searchtype)
#	else:
#		attrlist = locinfo(ldapobj, searchfor, type=searchtype)

	print "The following is the LDAP information for %s <br/>" % searchfor
	print "-------------------------------------------------------------------------------------------------------------------------------<br/>"
	if not attrlist:
		print "These is nothing more found for %s!!!<br/>" % searchfor
	for key in attrlist.keys():
		print key + ":	" + str(attrlist[key])
		print '<br/>'
	print '<br/>'

def locinfo(locs, searchvar, type="plocation"):
	hashhost = {}

	if type == "plocation":
		hashhost = hashhosts(searchvar)
		#pprint(hashhost)
		for dn, attr in locs:
			if attr.has_key('parent') and hashhost.has_key(attr['parent'][0]) and attr['section'][0] in hashhost[attr['parent'][0]]['section']:
				return attr
	if type == "hostname":
		for dn, attr in locs:
			if attr.has_key('location') and attr['location'][0] == searchvar:
				return attr
	if type == "ipaddr":
		for dn, attr in locs:
			if attr.has_key('interface') and strinlist(searchvar, attr['interface']):
				return attr
	return

def devinfo(devs, searchvar, type="macaddr"):
	if type == "macaddr":
		for dn, attr in devs:
			if attr.has_key('interface') and strinlist(searchvar, attr['interface']):
				return attr	
	if type == "hostname":
		for dn, attr in devs:
			if attr.has_key('location') and attr['location'][0] == searchvar:
				return attr
	return

def userinfo(users, searchvar, type="userid"):
	if type == "userid":
		for dn, attr in users:
			if attr.has_key('user') and strinlist(searchvar, attr['user']):
				return attr	
	return

def serviceinfo(services, searchvar):
	attrlist = {}
	for dn, attr in services:
		if attr.has_key('address') and strinlist(searchvar, attr['address']):
			attrlist[attr['service'][0]] = attr['service'][0]
	return attrlist

def getparent(ldapobj, parent):
	for dn, attr in ldapobj:
		if attr.has_key('location') and attr['location'][0] == parent:
			return attr
	return


def showhome():
	print '<br/> <a href="/" title="Please go back to homepage!">Please go back to homepage!</a>'

def main():

	print "Content-type:text/html\r\n\r\n"

	print_header()
	
	form = cgi.FieldStorage()
	
	searchfor = form.getvalue('searchfor')
	searchtype = form.getvalue('dropdown')


	if not searchfor or not searchtype:
		print """You should input the correct search string:<br/> 
		1. select a search type;  <br/>
		2. input corresponding search string  <br/><br/>"""
		showhome()
		sys.exit()
	
	# Gather LDAP login information
	# removed sensitive info here
	#
	
	# Bind to LDAP
	ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)
	l = ldap.initialize("ldap://ldap-vip.sample.net")
	l.start_tls_s()
	
	try:
	    l.simple_bind_s(dn, password)
	except ldap.INVALID_CREDENTIALS:
	    print("ERROR: invalid ldap credentials for jameszhu" )
	    sys.exit(1)
	
	
	locations = l.search_s("ou=locations,dc=sample,dc=net",ldap.SCOPE_ONELEVEL)
	devices = l.search_s("ou=devices,dc=sample,dc=net",ldap.SCOPE_ONELEVEL)
	services = l.search_s("ou=services,dc=sample,dc=net",ldap.SCOPE_ONELEVEL)
	users = l.search_s("ou=users,dc=sample,dc=net",ldap.SCOPE_ONELEVEL)

	if searchtype == "plocation":

		attrlist = locinfo(locations, searchfor, type=searchtype)
		prtinfo(attrlist, searchfor)
		hostname = attrlist['location'][0]
		devattrlist = devinfo(devices, hostname, type='hostname')
		prtinfo(devattrlist, hostname)
		parent = attrlist['parent'][0]
		parentlist = getparent(locations, parent)
		prtinfo(parentlist, attrlist['parent'][0])
		showhome()

	if searchtype == "hostname":
		attrlist = locinfo(locations, searchfor, type=searchtype)
		prtinfo(attrlist, searchfor)
		hostname = attrlist['location'][0]
		devattrlist = devinfo(devices, hostname, type='hostname')
		prtinfo(devattrlist, hostname)
		parent = attrlist['parent'][0]
		parentlist = getparent(locations, parent)
		prtinfo(parentlist, attrlist['parent'][0])
		showhome()

	if searchtype == "ipaddr":
		attrlist = locinfo(locations, searchfor, type=searchtype)
		prtinfo(attrlist, searchfor)
		hostname = attrlist['location'][0]
		devattrlist = devinfo(devices, hostname, type='hostname')
		prtinfo(devattrlist, hostname)
		parent = attrlist['parent'][0]
		parentlist = getparent(locations, parent)
		prtinfo(parentlist, attrlist['parent'][0])
		showhome()

	if searchtype == "macaddr":
		attrlist = devinfo(devices, searchfor, type=searchtype)
		prtinfo(attrlist, searchfor)
		hostname = attrlist['location'][0]
		locslist = locinfo(locations, hostname, type='hostname')
		prtinfo(locslist, hostname)
		showhome()

	if searchtype == "userid":
		attrlist = userinfo(users, searchfor, type=searchtype)
		prtinfo(attrlist, searchfor)
		showhome()

if __name__ == "__main__":
	main()
