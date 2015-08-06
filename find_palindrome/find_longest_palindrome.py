#!/usr/bin/python
import sys
from pprint import pprint

sys.setrecursionlimit(1000000)

longest = '';
pals = {};

def find_longest_palindrome(s):
    global longest
    global pals
    if len(s) == 1:
        return
    if s == s[::-1]:
        if len(s) > len(longest):
            longest = s
        if(pals.has_key(s)):
            pals[s]['n'] = pals[s]['n'] + 1
            pals[s]['l'] = len(s)
        else:
            pals[s] = {}
            pals[s]['n'] = 1
            pals[s]['l'] = len(s)
    else:
        find_longest_palindrome(s[:-1]);
   
s = sys.argv[1]
for i in xrange(len(s)):
    find_longest_palindrome(s[i:])

pprint(pals)
print "Longgest palindrome is: " + longest
