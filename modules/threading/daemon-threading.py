#!/usr/bin/env python
""" This is for learning threading
"""
import threading
import time


def nondaemonthread():
    """ Testing
    """
    print("starting my thread")
    time.sleep(8)
    print("ending my thread")


def daemonthread():
    """ Testing
    """
    while True:
        print("Hello")
        time.sleep(2)


if __name__ == '__main__':
    """ Testing
    """
    nondaemonthread = threading.Thread(target=nondaemonthread)
    daemonthread = threading.Thread(target=daemonthread)
    daemonthread.setDaemon(True)
    daemonthread.start()
    nondaemonthread.start()
