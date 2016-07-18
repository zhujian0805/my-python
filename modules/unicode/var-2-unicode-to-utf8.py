#!/usr/bin/python

# Checkout this thread: http://stackoverflow.com/questions/10268518/python-string-to-unicode
# I get a utf8 string from the internet, so it is actually a string of a lot of
# characters: '\', 'u', .....
string = '\u738b\u5e9c\u4e95\u5e97\u53cc\u4eba\u5957\u9910\uff01\u8282\u5047\u65e5\u901a\u7528\uff0c\u63d0\u4f9b\u514d\u8d39WiFi\uff01'

# To make unicode out of this, use decode('unicode-escape')

print string.decode('unicode-escape').encode('utf8')

# Or this is the same:
print string.decode('unicode-escape')
