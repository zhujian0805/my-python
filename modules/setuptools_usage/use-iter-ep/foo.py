# file foo.py
import pkg_resources
for ep in pkg_resources.iter_entry_points('fooo'):
    name = ep.name
    module = ep.load()
    print name
    print module
