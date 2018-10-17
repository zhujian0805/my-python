#!/usr/bin/python
import paramiko

t = paramiko.Transport(('主机', '端口'))
t.connect(username='用户名', password='口令')
sftp = paramiko.SFTPClient.from_transport(t)
remotepath = '/var/log/system.log'
localpath = '/tmp/system.log'
sftp.get(remotepath, localpath)
t.close()
