#!/usr/bin/python

# Checkout this thread: http://stackoverflow.com/questions/10268518/python-string-to-unicode
# I get a utf8 string from the internet, so it is actually a string of a lot of
# characters: '\', 'u', .....
string = '\u738b\u5e9c\u4e95\u5e97\u53cc\u4eba\u5957\u9910\uff01\u8282\u5047\u65e5\u901a\u7528\uff0c\u63d0\u4f9b\u514d\u8d39WiFi\uff01'

string = '0\x82\x02D\x02\x01\nc\x82\x02=\x04\x19ou=posix,dc=battle,dc=net\n\x01\x02\n\x01\x00\x02\x01\x00\x02\x01\x00\x01\x01\x00\xa0R\xa3\x0f\x04\x03uid\x04\x08ldap-vip\xa3\x1b\x04\x0bobjectclass\x04\x0cposixAccount\x87\x03uid\xa0\x1d\x87\tuidNumber\xa2\x10\xa3\x0e\x04\tuidNumber\x04\x0100\x82\x01\xbb\x04\x0bobjectClass\x04\x03uid\x04\x0cuserPassword\x04\tuidNumber\x04\tgidNumber\x04\x05gecos\x04\rhomeDirectory\x04\nloginShell\x04\x10krbPrincipalName\x04\x02cn\x04\x0fmodifyTimestamp\x04\x0fmodifyTimestamp\x04\x10shadowLastChange\x04\tshadowMin\x04\tshadowMax\x04\rshadowWarning\x04\x0eshadowInactive\x04\x0cshadowExpire\x04\nshadowFlag\x04\x10krbLastPwdChange\x04\x15krbPasswordExpiration\x04\x0cpwdAttribute\x04\x11authorizedService\x04\x0eaccountExpires\x04\x12userAccountControl\x04\rnsAccountLock\x04\x04host\x04\rloginDisabled\x04\x13loginExpirationTime\x04\x13loginAllowedTimeMap\x04\x0csshPublicKey'

# To make unicode out of this, use decode('unicode-escape')

print string.decode('unicode-escape').encode('utf8')

# Or this is the same:
print string.decode('unicode-escape')
