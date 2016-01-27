# file add.py
import os
 
 
def make():
    print "register %s" % os.path.splitext(os.path.basename(__file__))[0]

