#!/usr/bin/python

import json
from pprint import pprint

data = {}
data['data'] = []
data['data'].append([
    "Tiger Nixon", "System Architect", "Edinburgh", "5421", "2011/04/25",
    "$320,800"
])

print json.JSONEncoder().encode(data)
