#!/usr/bin/python

func_template = """def activate_field_%d(): print(%d)"""
for x in range(1, 11):
    exec (func_template % (x, x))

activate_field_1()
