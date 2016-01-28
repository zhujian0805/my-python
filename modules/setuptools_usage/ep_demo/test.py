#!/usr/bin/python

import pkg_resources

group = 'mypackage.api.v1'
for entrypoint in pkg_resources.iter_entry_points(group):
    # Grab the function that is the actual plugin.
    plugin = entrypoint.load()
    print plugin
    plugin()
