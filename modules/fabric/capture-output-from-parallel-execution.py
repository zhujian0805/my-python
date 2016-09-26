#!/usr/bin/python

from fabric.api import *

env.password = "123456"
env.skip_bad_hosts = True

class ParallelCommands():
    def __init__(self, **args):
        self.hosts = args['hosts']
        self.command = args['command']

    @parallel(pool_size=10) # Run on as many as 10 hosts at once
    def parallel_exec(self):
        return run(self.command)

    def capture(self):
        with settings(hide('running', 'commands', 'stdout', 'stderr')):
            stdout = execute(self.parallel_exec, hosts=self.hosts)
        return stdout

hosts = ['jzhu@localhost', 'test@localhost']
command = 'uname -a'

instance = ParallelCommands(hosts=hosts, command=command)
output = instance.capture()

"""
The output of each server is inside a dictionary:
{ 'root@server1': 'output', 'root@server2': 'output' }
"""

print output['jzhu@localhost'] 
print output['test@localhost'] 
