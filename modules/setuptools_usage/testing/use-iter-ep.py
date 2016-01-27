#!/usr/bin/python
from pkg_resources import iter_entry_points
for entry_point in iter_entry_points(group='cms.plugin', name=None):
    print(entry_point)
