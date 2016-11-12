#!/usr/bin/python3

import socket

with socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP) as s:
    while True:
        print(s.recvfrom(65565))
