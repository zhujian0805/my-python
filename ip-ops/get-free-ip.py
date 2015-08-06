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
from IPy import IP, IPSet

def getIpRange(l, site, domain):
    networks = l.search_s("ou=networks,dc=%s,dc=net" % domain, ldap.SCOPE_SUBTREE, "(network=%s)" % site)

    ips = []

    for dn, attrs in networks:
        if attrs['network'][0] == site and attrs.has_key('ip'):
            ips = IP(attrs['ip'][0])

    return ips

def getUsedIp(l, site, domain):
    usedip = []
    thesite = site.split('-')[0]

    locations = l.search_s("ou=locations,dc=%s,dc=net" % domain, ldap.SCOPE_SUBTREE, "(location=%s-*)" % thesite)

    for dn, attr in locations:
        if attr.has_key('interface'):
            for intf in attr['interface']:
                iiip = intf.split('=')[1]
                usedip.append(iiip)

    return usedip


def main(server, password, site, domain):
    dn = "user=jameszhu,ou=users,dc=%s,dc=net" % domain
    ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)
    conn_str = "ldap://" + server
    l = ldap.initialize(conn_str)
    l.start_tls_s()
	
    try:
        l.simple_bind_s(dn, password)
    except ldap.INVALID_CREDENTIALS:
        print("ERROR: invalid ldap credentials for jameszhu" )
        sys.exit(1)

    allips = getIpRange(l, site, domain)
    usedips = getUsedIp(l, site, domain)
    freeips = []

    for ip in allips:
        if str(ip) not in usedips:
            print ip


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
