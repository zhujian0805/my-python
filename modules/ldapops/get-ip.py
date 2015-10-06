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

def readLoctions(path):
    fh = open(path)
    lines = {}
    while True:
        line = fh.readline().strip()
        if line:
            cols = line.split()
            mykey = ''.join(cols)
            lines[mykey] = {}
            lines[mykey]['location'] = cols[0]
            lines[mykey]['slot'] = cols[1]
        else:
            break
    return lines            


def getMac(ip, slot, passwd):
    client = paramiko.client.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    paramiko.util.log_to_file('/tmp/' + sys.argv[0] + '.log')
    macs = [ 'XXXXXX', 'XXXXXX' ]
    try:
        client.connect(ip, port=22, username='me', password=passwd, timeout=10)
        stdin, stdout, stderr = client.exec_command('info -T system:blade[%s]'%slot)
        for line in stdout.readlines():
            if re.search(r'MAC Address 1:', line):
                cols = line.strip().split(':', 1)
                macs[0] = cols[1].strip()
            if re.search(r'MAC Address 2:', line):
                cols = line.strip().split(':', 1)
                macs[1] = cols[1].strip()
    except:
        pass

    return macs

def main(server, password, filepath, site):
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
	
	locations = l.search_s("ou=locations,dc=sample,dc=net",ldap.SCOPE_SUBTREE, "(location=%s-*)"%site)

        target = readLoctions(filepath)

        #pprint(target)
        
        for k in target.keys():
            t = target[k]['location']
            for dn, attrs in locations:
                intf = []
                if attrs.has_key('location'):
                    if attrs['location'][0] == t:
                        for i in attrs['interface']:
                            if re.search(r'mm', i):
                                ret = re.sub('mm.*=', '', i)
                                intf.append(ret)
                        slotnum = re.sub(r'\D*', '', target[k]['slot'])
                        mymacs = getMac(intf[0], slotnum, 'changeme')

                        if re.search(r'XXXX', mymacs[0]):
                            mymacs = getMac(intf[0], slotnum, '1St!E$GT$8')
                            if re.search(r'XXXX', mymacs[0]):
                                mymacs = getMac(intf[1], slotnum, 'changeme')
                                if re.search(r'XXXX', mymacs[0]):
                                    mymacs = getMac(intf[1], slotnum, '1St!E$GT$8')

                        print t, target[k]['slot'], intf[0], intf[1], mymacs[0], mymacs[1]

if __name__ == "__main__":
#    main(server, password, filepath, site):
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
