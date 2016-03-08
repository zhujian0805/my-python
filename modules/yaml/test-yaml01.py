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
    - Apple:
        Red:
          1000
    - Orange
    - Strawberry
    - Mango
languages:
    ruby: Elite
    python: Elite
    dotnet: Lame
company:
    - HP:
        - China:
        - Japan
    - IBM
                """)

print yyy


print yaml.dump( { 'name': "James Zhu", 'family': [ 'Nemo', "lily" ] } )
