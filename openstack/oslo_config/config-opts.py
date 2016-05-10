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

vxlan_opts = [
    cfg.BoolOpt('enable_vxlan', default=True,
                help=("Enable VXLAN on the agent. Can be enabled when "
                       "agent is managed by ml2 plugin using linuxbridge "
                       "mechanism driver")),
    cfg.IntOpt('ttl',
               help=("TTL for vxlan interface protocol packets.")),
    cfg.IntOpt('tos',
               help=("TOS for vxlan interface protocol packets.")),
    cfg.StrOpt('vxlan_group', default='DEFAULT_VXLAN_GROUP',
               help=("Multicast group(s) for vxlan interface. A range of "
                      "group addresses may be specified by using CIDR "
                      "notation. To reserve a unique group for each possible "
                      "(24-bit) VNI, use a /8 such as 239.0.0.0/8. This "
                      "setting must be the same on all the agents.")),
    cfg.IPOpt('local_ip', help=("Local IP address of the VXLAN endpoints.")),
    cfg.BoolOpt('l2_population', default=False,
                help=("Extension to use alongside ml2 plugin's l2population "
                       "mechanism driver. It enables the plugin to populate "
                       "VXLAN forwarding table.")),
]

cfg.CONF.register_opts(vxlan_opts, "VXLAN")

print cfg.CONF.VXLAN.ttl