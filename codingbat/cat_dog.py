#!/usr/bin/python

def cat_dog(str):
    cat = 0
    dog = 0
    for i in xrange(0,len(str)-2):
        s = str[i:i+3]
        if s == 'cat':
            cat = cat + 1
        if s == 'dog':
            dog = dog + 1
    if cat == dog:
        return True
    else:
        return False

print cat_dog("catdo")
