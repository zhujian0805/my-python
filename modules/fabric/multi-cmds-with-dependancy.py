#!/usr/bin/python

from fabric.api import run, sudo, env, cd

# Specify host here or on the cli with -H option
#env.hosts = ['host1', 'host2']

def taskA():
  with cd('/'):
    with cd('etc'):
      run('ls -ltr')
