#!/usr/bin/python

import yaml

yyy = yaml.load("""
---
# An employee record
name: |
        Martin
        D'vloper
""")

print yyy
