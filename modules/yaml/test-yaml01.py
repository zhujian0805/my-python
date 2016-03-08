#!/usr/bin/python

import yaml

yyy = yaml.load("""
---
# An employee record
name: Martin D'vloper
job: Developer
skill: Elite
employed: True
foods:
    - Apple
    - Orange
    - Strawberry
    - Mango
languages:
    ruby: Elite
    python: Elite
    dotnet: Lame
                """)

print yyy


print yaml.dump( { 'name': "James Zhu", 'family': [ 'Nemo', "lily" ] } )
