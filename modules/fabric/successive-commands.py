#!/usr/bin/python

from fabric.api import run, sudo, env

# Specify host here or on the cli with -H option
#env.hosts = ['host1', 'host2']

def taskA():
    run('cd /')
    run('ls -ltr')
