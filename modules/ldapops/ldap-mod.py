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

username = ''
#ldapserver = 'ldapmaster.sample.net'
ldapserver = sys.argv[1]


def conn_ldap():
    global ldapserver
    try:
        #    ldap.set_option(ldap.OPT_X_TLS, ldap.OPT_X_TLS_DEMAND)
        l = ldap.initialize('ldap://%s' % ldapserver)
        l.simple_bind_s('cn=manager,dc=sample,dc=net', 'sample1')
    except:
        print(
            "something is jacked with the ldap bind... see error for details")

    return l


def main():
    l = conn_ldap()
    #accounts = l.search_s('uid=*ntp*,ou=People,dc=sample,dc=net', ldap.SCOPE_SUBTREE)
    accounts = l.search_s('ou=People,dc=sample,dc=net', ldap.SCOPE_SUBTREE,
                          '(&(objectClass=account)(uid=dbus))')

    #    pprint(accounts)

    i = 'fuckyou'

    modlist1 = []
    item = (ldap.MOD_REPLACE, 'uid', i)
    modlist1.append(item)

    for dn, attrs in accounts:
        print dn
        print attrs
        print("modifying %s" % dn)

        try:
            l.modify_s(dn, modlist1)
        except ldap.TYPE_OR_VALUE_EXISTS:
            print "already"
        except ldap.NO_SUCH_ATTRIBUTE:
            print "the user doesn't have this attr"
        except Exception as ex:
            template = "An exception of type {0} occured. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print message
            sys.exit(1)


if __name__ == "__main__":
    main()
