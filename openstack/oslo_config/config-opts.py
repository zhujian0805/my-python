#!/usr/bin/python
from oslo_config import cfg
import sys

conf = cfg.ConfigOpts()
conf.register_opt(cfg.BoolOpt('verbose',))
conf(sys.argv[1:])
if conf.verbose:
  print "YES"
  

rabbit_host_opt = cfg.StrOpt('name',
                             default='localhost',
                             help='IP/hostname to listen on.')

conf.register_opt(rabbit_host_opt)

print conf.name

rabbit_group = cfg.OptGroup(name='testing',
                            title='testing')
rabbit_host_opt = cfg.StrOpt('host',
                             default='localhost',
                             help='IP/hostname to listen on.')

conf.register_group(rabbit_group)
conf.register_opt(rabbit_host_opt, group=rabbit_group)

print conf.testing.host
