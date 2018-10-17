#!/usr/bin/python
import rpyc
from rpyc.utils.server import ThreadedServer
from rpyc.lib import setup_logger
import sys
import logging


class MyService(rpyc.Service):
    def on_connect(self):
        pass

    def on_disconnect(self):
        pass

    def exposed_get_answer(self):    # this is an exposed method
        return 42

    def get_question(self):    # while this method is not exposed
        return "what is the airspeed velocity of an unladen swallow?"


if __name__ == "__main__":
    t = ThreadedServer(MyService, port=8080, auto_register=1)
    logging.warn("AHA\n")
    t.start()
