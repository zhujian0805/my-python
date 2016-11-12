#!/usr/bin/python3

import socket
from struct import unpack

with socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP) as s:
#with socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(0x0003)) as s:
    while True:
        raw_packet = s.recvfrom(65565)
        packet = raw_packet[0]
        raw_iph = packet[0:20]
        # unpack(fmt, buffer) - 根据指定的格式化字符串来拆解给定的buffer
        # B 单字节的整型
        # H 双字节的整型
        # s bytes，前加数字表示取4字节的bytes
        iph = unpack("!BBHHHBBH4s4s", raw_iph)
        fields = {}
        fields["Version"] = iph[0] >> 4  # 版本字段与IP数据报头部共享一个字节，通过右移操作取得单独的版本字段
        fields["IP Header Length"] = (iph[0] & 0xF) * 4  # 首部长度字段的1代表4个字节
        fields["Type of Service"] = iph[1]  # 区分服务，一般情况下并不使用
        fields["Total Length"] = iph[2]  # IP首部+数据的总长度，即len(packet)
        fields["Identification"] = iph[3]  # 标识
        flags = iph[4] >> 13  # 标识位与片偏移共享2个字节，且最高位并且未使用
        fields["MF"] = 1 if flags & 1 else 0  # 测试最低位
        fields["DF"] = 1 if flags & 1 else 0  # 测试中间位
        fields["Fragment Offset"] = iph[4] & 0x1FFF  # 位与操作取得片偏移
        fields["Time to Live"] = iph[5]  # 生存时间，单位是跳数
        fields["Protocol"] = iph[6]  # 数据报携带的数据使用的协议，TCP为6
        fields["Header Checksum"] = iph[7]  # 首部校验和
        # socket.inet_ntoa(..)
        # - convert an ip address from 32-bit packed binary format to string format
        fields["Source Address"] = socket.inet_ntoa(iph[8])
        fields["Destination Address"] = socket.inet_ntoa(iph[9])

        for k, v in fields.items():  # 遍历打印，由于是dict，因此打印是无序的
            print(k, ':', v)
        print("")
