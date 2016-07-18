[LINK]
http://www.grotan.com/ldap/python-ldap-samples.html


[Contents]
The original file is available here.
python-ldap sample code

    Bind
    Add
    Modify
    Search
    Delete

Binding to LDAP Server
Simple Authentication

import ldap
try:
    l = ldap.open("127.0.0.1")
    
    # you should  set this to ldap.VERSION2 if you're using a v2 directory
    l.protocol_version = ldap.VERSION3
    # Pass in a valid username and password to get 
    # privileged directory access.
    # If you leave them as empty strings or pass an invalid value
    # you will still bind to the server but with limited privileges.
    
    username = "cn=Manager, o=anydomain.com"
    password  = "secret"
    
    # Any errors will throw an ldap.LDAPError exception 
    # or related exception so you can ignore the result
    l.simple_bind(username, password)
except ldap.LDAPError, e:
    print e
    # handle error however you like
    
                            

Adding entries to an LDAP Directory
Synchrounous add

# import needed modules
import ldap
import ldap.modlist as modlist

# Open a connection
l = ldap.initialize("ldaps://localhost.localdomain:636/")

# Bind/authenticate with a user with apropriate rights to add objects
l.simple_bind_s("cn=manager,dc=example,dc=com","secret")

# The dn of our new entry/object
dn="cn=replica,dc=example,dc=com" 

# A dict to help build the "body" of the object
attrs = {}
attrs['objectclass'] = ['top','organizationalRole','simpleSecurityObject']
attrs['cn'] = 'replica'
attrs['userPassword'] = 'aDifferentSecret'
attrs['description'] = 'User object for replication using slurpd'

# Convert our dict to nice syntax for the add-function using modlist-module
ldif = modlist.addModlist(attrs)

# Do the actual synchronous add-operation to the ldapserver
l.add_s(dn,ldif)

# Its nice to the server to disconnect and free resources when done
l.unbind_s()

                            

Modify entries in an LDAP Directory
Synchrounous modify

# import needed modules
import ldap
import ldap.modlist as modlist

# Open a connection
l = ldap.initialize("ldaps://localhost.localdomain:636/")

# Bind/authenticate with a user with apropriate rights to add objects
l.simple_bind_s("cn=manager,dc=example,dc=com","secret")

# The dn of our existing entry/object
dn="cn=replica,dc=example,dc=com" 

# Some place-holders for old and new values
old = {'description':'User object for replication using slurpd'}
new = {'description':'Bind object used for replication using slurpd'}

# Convert place-holders for modify-operation using modlist-module
ldif = modlist.modifyModlist(old,new)

# Do the actual modification 
l.modify_s(dn,ldif)

# Its nice to the server to disconnect and free resources when done
l.unbind_s()
                            

Searching an LDAP Directory
Asynchronous Search

import ldap

## first you must open a connection to the server
try:
    l = ldap.open("127.0.0.1")
    ## searching doesn't require a bind in LDAP V3.  If you're using LDAP v2,
set the next line appropriately
    ## and do a bind as shown in the above example.
    # you can also set this to ldap.VERSION2 if you're using a v2 directory
    # you should  set the next option to ldap.VERSION2 if you're using a v2
    # directory
    l.protocol_version = ldap.VERSION3
except ldap.LDAPError, e:
    print e
    # handle error however you like


## The next lines will also need to be changed to support your search
requirements and directory
baseDN = "ou=Customers, ou=Sales, o=anydomain.com"
searchScope = ldap.SCOPE_SUBTREE
## retrieve all attributes - again adjust to your needs - see documentation
for more options
retrieveAttributes = None 
searchFilter = "cn=*jack*"

try:
    ldap_result_id = l.search(baseDN, searchScope, searchFilter,
retrieveAttributes)
    result_set = []
    while 1:
        result_type, result_data = l.result(ldap_result_id, 0)
        if (result_data == []):
            break
        else:
            ## here you don't have to append to a list
            ## you could do whatever you want with the individual entry
            ## The appending to list is just for illustration. 
            if result_type == ldap.RES_SEARCH_ENTRY:
                result_set.append(result_data)
    print result_set
except ldap.LDAPError, e:
    print e

                            

Deleting an entry from an LDAP Server
Synchronous Delete

import ldap

## first you must bind so we're doing a simple bind first
try:
    l = ldap.open("127.0.0.1")
    
    l.protocol_version = ldap.VERSION3
    # Pass in a valid username and password to get 
    # privileged directory access.
    # If you leave them as empty strings or pass an invalid value
    # you will still bind to the server but with limited privileges.
    
    username = "cn=Manager, o=anydomain.com"
    password  = "secret"
    
    # Any errors will throw an ldap.LDAPError exception 
    # or related exception so you can ignore the result
    l.simple_bind(username, password)
except ldap.LDAPError, e:
    print e
    # handle error however you like


# The next lines will also need to be changed to support your requirements and
# directory
deleteDN = "uid=anyuserid,
ou=Customersprotectedu=Salesprotected=anydomain.com"
try:
    # you can safely ignore the results returned as an exception 
    # will be raised if the delete doesn't work.
    l.delete_s(deleteDN)
except ldap.LDAPError, e:
    print e
    ## handle error however you like
                            


