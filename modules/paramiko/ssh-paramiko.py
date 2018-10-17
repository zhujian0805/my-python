#!/usr/bin/python
import paramiko.client
import sys
import re


def get_mac(ip, slot):
    client = paramiko.client.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    paramiko.util.log_to_file('/tmp/' + sys.argv[0] + '.log')
    try:
        client.connect(ip, port=22, username='me', password='changeme')
        stdin, stdout, stderr = client.exec_command(
            'info -T system:blade[%s]' % slot)
        for line in stdout.readlines():
            if re.search(r'MAC Address 1', line):
                cols = line.strip().split(':', 1)
                print cols[1].strip()
            if re.search(r'MAC Address 2', line):
                cols = line.strip().split(':', 1)
                print cols[1].strip()
    except:
        print "something wrong!"


if __name__ == '__main__':
    get_mac(sys.argv[1], sys.argv[2])
