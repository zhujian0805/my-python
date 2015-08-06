#!/usr/bin/python

LIST = [['A', '1'], ['B', '2'], ['C', '3'], ['A', '4'], ['B', '5'], ['C', '6'], ['A', '1'], ['B', '1'], ['C', '1']]
DICT={}

for i in LIST:
  if DICT.has_key(i[0]):
    DICT[i[0]] = DICT[i[0]] + int(i[1])
  else:
    DICT[i[0]] = int(i[1])

print DICT
