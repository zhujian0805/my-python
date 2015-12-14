#!/usr/bin/python

from fabric.api import run, sudo, env

# Specify host here or on the cli with -H option
#env.hosts = ['host1', 'host2']

def taskA():
    run('ls')

def taskB():
    run('whoami')

def taskC():
    run('cat /etc/passwd')

def taskD():
    sudo('touch /etc/testing-file')

def taskAll():
    taskA()
    taskB()
    taskC()
    taskD()
