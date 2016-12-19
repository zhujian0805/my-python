#!/usr/bin/python
import struct

# Extract the 4-7 from a string
data = struct.unpack("3x3s", 'abcefg')

print data
