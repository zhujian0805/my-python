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
import paramiko.client

def main(server, password, location):
        # Gather LDAP login information
	dn = "user=jameszhu,ou=users,dc=sample,dc=net"
	# Bind to LDAP
	ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)
        conn_str = "ldap://" + server
        l = ldap.initialize(conn_str)
	l.start_tls_s()
	
	try:
	    l.simple_bind_s(dn, password)
	except ldap.INVALID_CREDENTIALS:
	    print("ERROR: invalid ldap credentials for jameszhu" )
	    sys.exit(1)
	
	locations = l.search_s("ou=locations,dc=sample,dc=net",ldap.SCOPE_SUBTREE, "(location=*%s*)" % location)

        ips = []
        for dn, attrs in locations:
            print attrs['location'][0] + ' ' +  attrs['interface'][0]


if __name__ == "__main__":
#    main(server, password, filepath, site):
    main(sys.argv[1], sys.argv[2], sys.argv[3])
