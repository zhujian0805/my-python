#!/usr/bin/python
from multiprocessing import Process, Queue, current_process, freeze_support
import sys
import getpass
import os, time
import pexpect
from pprint import pprint


def ssh_command(user, password, command, input, output):
    """
    This runs a command on the remote host. This could also be done with the
    pxssh class, but this demonstrates what that class does at a simpler level.
    This returns a pexpect.spawn object. This handles the case when you try to
    connect to a new host and ssh asks you if you want to accept the public key
    fingerprint and continue connecting.
    """
    ssh_newkey = 'Are you sure you want to continue connecting'

    for host in iter(input.get, 'STOP'):
        child = pexpect.spawn(
            'ssh -l %s %s %s' % (user, host, command), timeout=30)
        child.logfile = sys.stdout
        i = child.expect([pexpect.TIMEOUT, ssh_newkey, 'password: '])
        if i == 0:
            print 'ERROR!'
            print 'SSH could not login. Here is what SSH said:'
            print child.before, child.after
            return None
        if i == 1:
            child.sendline('yes')
            child.expect('password: ')
            i = child.expect([pexpect.TIMEOUT, 'password: '])
            if i == 0:
                print 'ERROR!'
                print 'SSH could not login. Here is what SSH said:'
                print child.before, child.after
                return None
        child.sendline(password)
        child.expect(pexpect.EOF)
        print child.before.strip()


def gethosts(hostfile):
    hosts = []
    try:
        fh = open(hostfile)
    except:
        print >> sys.stderr, "File could not be opened"
        sys.exit(1)
    while True:
        line = fh.readline()
        if line:
            hosts.append(line.strip())
        else:
            break
    fh.close()
    return hosts


def main():
    processes = []
    if (len(sys.argv) != 2):
        print "Usage: %s NUM_OF_PROCESS" % sys.argv[0]
        sys.exit(1)

    user = raw_input('Username: ')
    password = getpass.getpass()
    command = raw_input('Enter the command: ')
    hosts = []
    hosts = gethosts("hosts.txt")
    task_queue = Queue()
    done_queue = Queue()

    for task in hosts:
        task_queue.put(task)

    NUMBER_OF_PROCESSES = int(sys.argv[1])

    for i in range(NUMBER_OF_PROCESSES):
        p = Process(
            target=ssh_command,
            args=(user, password, command, task_queue, done_queue))
        p.start()
        processes.append(p)

    while not task_queue.empty():
        time.sleep(1)

    for i in range(NUMBER_OF_PROCESSES):
        task_queue.put('STOP')

    for proc in processes:
        proc.join()


if __name__ == '__main__':
    freeze_support()
    main()
