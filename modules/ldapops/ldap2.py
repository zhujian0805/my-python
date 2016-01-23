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

    for dn, attrs in locations:
        if attrs.has_key('location'):
            print attrs['location'][0]


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
