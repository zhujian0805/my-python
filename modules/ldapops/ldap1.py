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


def main(server, password):

    # Gather LDAP login information
    dn = "user=jameszhu,ou=users,dc=sample,dc=net"

    mylist = [
        '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13',
        '14'
    ]

    # Bind to LDAP
    ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)
    conn_str = "ldap://" + server
    l = ldap.initialize(conn_str)
    l.start_tls_s()

    try:
        l.simple_bind_s(dn, password)
    except ldap.INVALID_CREDENTIALS:
        print("ERROR: invalid ldap credentials for jameszhu")
        sys.exit(1)

    locations = l.search_s("ou=locations,dc=sample,dc=net", ldap.SCOPE_SUBTREE,
                           "(location=cn1-*)")
    #locations = l.search_s("ou=locations,dc=sample,dc=net",ldap.SCOPE_SUBTREE, "(location=cn1-*)")

    locs = {}
    for dn, attrs in locations:
        if attrs.has_key("parent") and attrs.has_key("section"):
            if not locs.has_key(attrs["parent"][0]):
                locs[attrs["parent"][0]] = []
                locs[attrs["parent"][0]].append(attrs["section"][0])
            else:
                locs[attrs["parent"][0]].append(attrs["section"][0])

    for k in locs.keys():
        if re.search(r'cn.*rack06.*',
                     k) or (not re.search(r'cn.*rack.*enclosure.*', k)):
            continue
        miss = findit(mylist, locs[k])
        for m in miss:
            print "%s slot %s" % (k, m)


def findit(l1, l2):
    ll = []
    for i1 in l1:
        count = 0
        for i2 in l2:
            i2 = re.sub('\D*', '', i2)
            if re.search(i1, i2):
                count = count + 1
        if count == 0:
            ll.append(i1)
    return ll


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
