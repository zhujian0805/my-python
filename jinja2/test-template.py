#!/usr/bin/python

from jinja2 import Template

aaa = ['one', 'two', 'three']

template = Template('Hello {{ name|join("-") }}!')
print template.render(name=aaa)
