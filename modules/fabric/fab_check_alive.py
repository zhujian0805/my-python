#!/usr/bin/python

""" This is a simplest fabric script"""
from fabric.api import sudo, env, execute, hide, cd
import paramiko, socket


env.hosts = ['localhost', '128.0.0.1']
env.user = "jzhu"
env.port = 22
env.password = "VFR$bgt5nhy6"
env.skip_bad_hosts = True
env.parallel = True
env.timeout = 1

def isup(host, port):
    """check if host alive"""
    orig_timeout = socket.getdefaulttimeout()
    timeout = 3
    socket.setdefaulttimeout(timeout)
    up = False
    try:
        transport = paramiko.Transport((host, port))
        up = True
    except:
        print('***Warning*** Host {host} on port {port} is down.'.format( host=host, port=port))
    socket.setdefaulttimeout(orig_timeout)
    return up

def hello(directory):
    """This is for a demostration of fabric"""
    ret = []
    if not isup(env.host, env.port):
        return "Host %s is not reachable from %i" % (env.host, env.port)
    with hide('aborts', 'status', 'running', 'stdout', 'stderr', 'warnings'):
        try:
            with cd(directory):
                myls = sudo("fink")
                ret.append(myls)
        except:
            ret.append("Failed to execute command")

    return ret

#execute(hello, "/dev")
OUTPUT = execute(hello, "/tmp")

print OUTPUT
