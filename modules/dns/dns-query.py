#!/usr/bin/python

import dns.resolver
 
myResolver = dns.resolver.Resolver()
myResolver.nameservers = ['8.8.8.8', '8.8.4.4']
 
try:
        myAnswers = myResolver.query("google.com", "A")
        for rdata in myAnswers:
                print rdata
except:
        print "Query failed"
