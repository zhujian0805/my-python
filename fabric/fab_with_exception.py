#!/usr/bin/python

""" This is a simplest fabric script"""
from fabric.api import sudo, env, execute, hide, cd
import StringIO


env.hosts = ['jameszhu@localhost:22', 'jameszhu@128.0.0.1:22']
env.password = "VFR$bgt5nhy6"
env.skip_bad_hosts = True
env.parallel = True
env.timeout = 1

def hello(directory):
    """This is for a demostration of fabric"""
    ret = []
    with hide('aborts', 'status', 'running', 'stdout', 'stderr', 'warnings'):
        try:
            with cd(directory):
                myls = sudo("find /")
                ret.append(myls)
        except:
            ret.append("Failed to execute command")

    return ret

#execute(hello, "/dev")
OUTPUT = execute(hello, "/tmp")

print OUTPUT
