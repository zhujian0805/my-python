#!/usr/bin/python3
import socket

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect(("127.0.0.1", 56789))
    s.send(b'Hello, world')
    data = s.recv(65565)
    print('Received', str(data))
