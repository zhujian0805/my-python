#!/usr/bin/python
import asyncore
import socket
import sys
import logging
from pprint import pprint
import re


class EchoHandler(asyncore.dispatcher_with_send):

    helpstr = """
avialable commands:
-----------------------
name        register your name with the chat server
chat        start to chat with everyone
bye         quit the chat
help|?      print this help
"""

    def __init__(self, sock):
        asyncore.dispatcher_with_send.__init__(self, sock)
        self.logger = logging.getLogger("EchoHandler")
        self.send(EchoHandler.helpstr)

    def handle_read(self):
        data = self.recv(8192)
        name = None
        if data:
            self.logger.debug("received %s" % data)
            #self.send("chat>")
            if data.strip() == "bye":
                self.handle_close()
            if data.strip() == "help" or data.strip() == "?":
                self.send(EchoHandler.helpstr)
                #self.send("chat>")
            searchobj = re.match(r'name(.*)', data.strip())
            the_key = str(self.addr[0]) + "." + str(self.addr[1])
            if searchobj:
                name = searchobj.group(1).strip()
                for user in users:
                    if user.has_key(the_key):
                        user[the_key]['name'] = name
            self.broadcast(data)

    def handle_error(self):
        self.logger.debug("Error, %s:%s is omitting error" % (
            (str(self.addr[0])), str(self.addr[1])))

    def handle_close(self):
        self.logger.debug("Hello, %s:%s is closing" % (
            (str(self.addr[0])), str(self.addr[1])))
        ###remove the closed socket from users
        closed = None
        the_key = str(self.addr[0]) + "." + str(self.addr[1])
        for user in users:
            if user.has_key(the_key):
                closed = user

        if closed:
            users.remove(closed)
            self.logger.debug(
                "removing socket %s from socket set" % str(closed))

        self.close()

    def create_file(self, fn):
        path = "/tmp/"
        fn = path + fn
        fo = open(fn, 'w')
        fo.close()

    def broadcast(self, data):
        my_key = str(self.addr[0]) + "." + str(self.addr[1])
        myname = my_key
        for user in users:
            if user.has_key(my_key):
                if user[my_key].has_key('name'):
                    myname = user[my_key]['name']

        self.logger.debug("broadcast: %s %s" % (my_key, myname))

        try:
            for user in users:
                self.logger.debug("my_key:" + my_key)
                if user.has_key(my_key):
                    self.logger.debug("sending to myself!!!")
                    if user[my_key].has_key('name'):
                        user[my_key]['sock'].send("\n" + user[my_key]['name'] +
                                                  " said> " + data)
                        user[my_key]['sock'].send(user[my_key]['name'] +
                                                  " said> ")
                        myname = user[my_key]['name']
                        self.logger.debug("my self name is :::: %s" % myname)
                    else:
                        user[my_key]['sock'].send("You said> ")
                else:
                    self.logger.debug("sending to others!!!")
                    others_key = user.keys()[0]
                    #self.logger.debug("others_key:" + others_key)
                    user[others_key]['sock'].send("\n" + myname + " said> " +
                                                  data)

                    if user[others_key].has_key('name'):
                        user[others_key]['sock'].send(
                            user[others_key]['name'] + " said> ")
                    else:
                        user[others_key]['sock'].send("You said> ")

        except Exception as ex:
            # in python 2.4/2.5, you should use the syntax as below line, chaning the "as"
            # to ","
            #except Exception , ex:
            self.logger.debug("exception in broadcast!")
            template = "An exception of type {0} occured. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print message


class EchoServer(asyncore.dispatcher):
    def __init__(self, host, port):
        self.logger = logging.getLogger("EchoServer")
        self.logger.debug("Starting server")
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(5)

    def handle_accept(self):
        pair = self.accept()
        self.logger.debug("executing handle_accept")
        user = {}
        if pair is not None:
            #users.append(list(pair))
            sock, addr = pair
            self.logger.debug(pair)
            the_key = str(addr[0]) + "." + str(addr[1])
            user[the_key] = {}
            user[the_key]['sock'] = sock
            user[the_key]['addr'] = addr
            users.append(user)
            self.logger.debug('Incoming connection from %s' % repr(addr))
            handler = EchoHandler(sock)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(name)s: %(message)s',
    )
    logger = logging.getLogger(sys.argv[0] + __name__)
    users = []
    server = EchoServer('0.0.0.0', 8080)
    asyncore.loop()
