#!/usr/bin/python
import sys
import ldap

def isAparent(locations, loc):
    location = ''
    if loc[1].has_key('location'):
        location = loc[1]['location'] 
    for dn, attrs in locations:
        if attrs.has_key('parent') and attrs['parent'] == location:
            return 1
    return 0

def hasBadserver(locations, parent):
    server = ''
    location = ''
    if parent[1].has_key('server'):
    	server = parent[1]['server'][0]
    if parent[1].has_key('location'):
    	location = parent[1]['location'][0]

    for dn, attrs in locations:
	
	if attrs.has_key('parent') and attrs['parent'][0] == location:
	    if attrs.has_key('server') and attrs['server'][0] != server:
		return 1
    return 0

def main(server, password, domain):
    ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)
    dn = "user=jameszhu,ou=users,dc=%s,dc=net" % domain
    conn_str = "ldap://" + server
    l = ldap.initialize(conn_str)
    l.start_tls_s()
	
    try:
        l.simple_bind_s(dn, password)
    except ldap.INVALID_CREDENTIALS:
        print("ERROR: invalid ldap credentials for jameszhu" )
        sys.exit(1)

    locations = l.search_s("ou=locations,dc=%s,dc=net" % domain, ldap.SCOPE_SUBTREE, "(|(location=*)(location=*))")
    parent = []
    for loc in locations:
        if isAparent(locations, loc):
            parent.append(loc)
    #pprint(parent)
    print "start processing.........."
    for l in parent:
	if hasBadserver(locations, l):
	    print l[0]

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3])
