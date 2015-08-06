#!/usr/bin/python

import hpilo

myilo = hpilo.Ilo("IP Addr", login="username", password="XXXX")

print(myilo.get_fw_version())
