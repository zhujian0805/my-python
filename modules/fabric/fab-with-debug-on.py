#!/usr/bin/python
from fabric.context_managers import settings
from fabric.api import run, sudo, env, cd, show

""" This is a simplest fabric script"""
def hello():
    """Hello function"""
    with show('debug'):
        run('find /tmp/ -ls')
