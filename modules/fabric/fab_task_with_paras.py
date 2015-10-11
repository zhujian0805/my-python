#!/usr/bin/python

""" This is a simplest fabric script"""
from fabric.api import sudo, env, execute, hide, cd
import StringIO
from pprint import pprint


env.hosts = ['jzhu@localhost:22', 'jzhu@127.0.0.1:22']
env.password = "123456"
env.skip_bad_hosts = True
env.parallel = True

def hello(directory):
    """This is for a demostration of fabric"""
    ret = []
    with hide('aborts', 'status', 'running', 'stdout', 'stderr', 'warnings'):
        try:
            with cd(directory):
                myls = sudo("find")
                ret.append(myls)
        except:
            ret.append("failed to execute command")

    return ret

#execute(hello, "/dev")
OUTPUT = execute(hello, "/tmp")

for host in OUTPUT:
  print host
  print '-----------------------'
  for i in OUTPUT[host][0].split("\n"):
    print i
