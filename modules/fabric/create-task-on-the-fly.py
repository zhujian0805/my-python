#!/usr/bin/python

from fabric.api import run, sudo, env

cmds = ['ls', 'hostname', 'uname -r']

tasks = []

def taskAll():
  for cmd in cmds:
    run(cmd)
