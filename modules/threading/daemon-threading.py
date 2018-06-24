#!/usr/bin/env python
"""
This is for learning threading
"""
import threading
import time

def nonDaemonThread():
    """ Testing """
    print("starting my thread")
    time.sleep(8)
    print("ending my thread")
def daemonThread():
    """ Testing """
    while True:
        print("Hello")
        time.sleep(2)
if __name__ == '__main__':
    nonDaemonThread = threading.Thread(target=nonDaemonThread)
    daemonThread = threading.Thread(target=daemonThread)
    daemonThread.setDaemon(True)
    daemonThread.start()
    nonDaemonThread.start()
