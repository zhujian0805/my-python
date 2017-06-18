#!/usr/bin/python

from jinja2 import Template

v = {'k1': 'one', 'k2': 'two'}
k = ['k1', 'k2']

template = Template('{{ a[b[0]] }}')
print(template.render(a=v, b=k))

template = Template('{% for i in b %} {{ a[i] }} {% endfor %}')
print(template.render(a=v, b=k))
