#!/usr/bin/python

big_integer = 1234325231

print type(big_integer)

print '{0:,d}'.format(big_integer)

big_float = 1234325231.00

print type(big_float)

print '{0:,f}'.format(big_float)

print '{0:,.2f}'.format(big_float)

print '{0:,.0f}'.format(big_float)
