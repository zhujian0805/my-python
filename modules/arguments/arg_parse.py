#!/usr/bin/python

import argparse

parser = argparse.ArgumentParser(
    description='This is a demostration',
    formatter_class=
    lambda prog: argparse.HelpFormatter(prog, max_help_position=35, width=130))
parser.add_argument("arg1", help="This is the first arg")
parser.add_argument(
    "-v",
    "--verbosity",
    help="increase output verbosity",
    required=True,
    type=int,
    choices=[0, 1, 2])
parser.add_argument(
    "-d", "--debug", help="increase output debug", action="count")
parser.add_argument("-a", "--array", dest="array", nargs="+")
parser.add_argument("arg2", help="This is the second arg")
args = parser.parse_args()

print "--------START----------------"
print args.arg1
print args.arg2
print args.verbosity
print args.debug
print args.array
