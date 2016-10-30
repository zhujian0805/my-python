#!/usr/bin/python
import socket
import fcntl
import struct
import sys


def getHwAddr(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    info = fcntl.ioctl(s.fileno(), 0x8927, struct.pack('256s', ifname[:15]))
    return ''.join(['%02x:' % ord(char) for char in info[18:24]])[:-1]


if __name__ == '__main__':
    print getHwAddr(sys.argv[1])
