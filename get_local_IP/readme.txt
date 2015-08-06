[Link]
http://www.pythonclub.org/python-network-application/get-ip-address

http://www.microhowto.info/howto/get_the_ip_address_of_a_network_interface_in_c_using_siocgifaddr.html


[Description]
使用Python获得本机IP地址

使用Python可以用很简单的方法得到本机IP地址，不过在Windows和Linux下的方法稍有不一样的，
Windows下获得IP地址的方法
方法一

使用拨号上网的话，一般都有一个本地ip和一个外网ip，使用python可以很容易的得到这两个ip
使用gethostbyname和gethostbyname_ex两个函数可以实现

import socket
localIP = socket.gethostbyname(socket.gethostname())#得到本地ip
print "local ip:%s "%localIP
 
ipList = socket.gethostbyname_ex(socket.gethostname())
for i in ipList:
    if i != localIP:
       print "external IP:%s"%i

方法二

import socket
 
myname = socket.getfqdn(socket.gethostname())
myaddr = socket.gethostbyname(myname)

Linux下获得IP地址的方法

上面的方法在Linux下也可以使用，除此之外，Linux下还可以用下面的方法得到本机IP地址。

Uses the Linux SIOCGIFADDR ioctl to find the IP address associated with a
network interface, given the name of that interface, e.g. “eth0”. The address
is returned as a string containing a dotted quad.

import socket
import fcntl
import struct
 
def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])

