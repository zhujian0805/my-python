#!/usr/bin/python

import cmd

class mycmd(cmd.Cmd):

    def __init__(self):
        cmd.Cmd.__init__(self)
        self.prompt = ">>>>"

    def default(self, line):
        print line

mycli = mycmd()

mycli.cmdloop()
