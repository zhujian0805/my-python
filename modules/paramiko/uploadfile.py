#!/usr/bin/python
import paramiko

t = paramiko.Transport('localhost', 22)
t.connect(username=jameszhu, password='123456')
sftp = paramiko.SFTPClient.from_transport(t)
remotepath = '/var/log/system.log'
localpath = '/tmp/system.log'
sftp.put(localpath, remotepath)
t.close()
