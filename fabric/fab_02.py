#!/usr/bin/python

""" This is a simplest fabric script"""
from fabric.api import sudo, env, execute


env.hosts = ['root@localhost:22']
env.password = '123456'

def hello():
    """This is for a demostration of fabric"""
    sudo("ls /etc")


execute(hello)
