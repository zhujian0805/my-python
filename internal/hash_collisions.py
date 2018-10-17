#!/usr/bin/python
"""http://www.shutupandship.com/2012/02/how-hash-collisions-are-resolved-in.html
"""


class C(object):
    def __hash__(self):
        return 42

    def __eq__(self, other):
        return False


d = {C(): 1, C(): 2, C(): 3}

print d
