#!/usr/bin/python
#
# THIS IS STILL IN TESTING!!!
#
import getpass
import sys, getopt
import os
import ldap
from pprint import pprint
import time
import ldap.modlist as modlist

username = 'jzhu'
ldapserver = 'ldapmaster.test.net'

#ldapserver = sys.argv[1]


def conn_ldap():
    global ldapserver
    try:
        #    ldap.set_option(ldap.OPT_X_TLS, ldap.OPT_X_TLS_DEMAND)
        ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)
        l = ldap.initialize('ldap://%s' % ldapserver)
        l.start_tls_s()
        l.simple_bind_s('user=jzhu,ou=users,dc=test,dc=net', 'PASSWORD')
    except:
        print(
            "something is jacked with the ldap bind... see error for details")

    return l


def main(oldlocation, newlocation):
    print("Renamed %s to %s" % (oldlocation, newlocation))
    l = conn_ldap()
    location = l.search_s(
        'location=%s,ou=locations,dc=test,dc=net' % oldlocation,
        ldap.SCOPE_SUBTREE)
    #accounts = l.search_s('ou=locations,dc=test,dc=net', ldap.SCOPE_SUBTREE, '(&(objectClass=account)(uid=dbus))')

    #    pprint(accounts)

    for dn, attrs in location:
        #print("modifying %s" % dn)

        try:
            # Important here, the RDN should be in format: "uid=XXX"
            l.modrdn_s(dn, 'location=%s' % newlocation)
        except Exception as ex:
            template = "An exception of type {0} occured. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print message
            sys.exit(1)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
