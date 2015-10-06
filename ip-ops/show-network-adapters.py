#!/usr/bin/python
import platform
import fcntl
import socket
import array
import struct
from pprint import pprint

ARCH_32_BIT = '32bit'
ARCH_64_BIT = '64bit'

def _get_linux_network_adapters():
    """Get the list of Linux network adapters."""
    import fcntl
    max_bytes = 8096
    arch = platform.architecture()[0]
    if arch == ARCH_32_BIT:
        offset1 = 32
        offset2 = 32
    elif arch == ARCH_64_BIT:
        offset1 = 16
        offset2 = 40
    else:
        raise OSError(_("Unknown architecture: %s") % arch)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    names = array.array('B', '\0' * max_bytes)
    outbytes = struct.unpack('iL', fcntl.ioctl(
        sock.fileno(),
        0x8912,
        struct.pack('iL', max_bytes, names.buffer_info()[0])))[0]
    adapter_names = [names.tostring()[n_cnt:n_cnt + offset1].split('\0', 1)[0]
                     for n_cnt in xrange(0, outbytes, offset2)]
    network_adapters = []
    for adapter_name in adapter_names:
        ip_address = socket.inet_ntoa(fcntl.ioctl(
            sock.fileno(),
            0x8915,
            struct.pack('256s', adapter_name))[20:24])
        subnet_mask = socket.inet_ntoa(fcntl.ioctl(
            sock.fileno(),
            0x891b,
            struct.pack('256s', adapter_name))[20:24])
        network_adapters.append({'name': adapter_name,
                                 'ip-address': ip_address,
                                 'subnet-mask': subnet_mask})
    return network_adapters

pprint(_get_linux_network_adapters())
