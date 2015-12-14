#!/usr/bin/python

import hpilo

myilo = hpilo.Ilo("ip addr", login="username", password="password")

print(myilo.get_server_name())
