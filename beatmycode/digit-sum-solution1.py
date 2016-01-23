#!/usr/bin/python
import sys
sum = 0


#BMC_TEST_INPUT_MAGIC=sys.argv[1]
def sum_single_digit(d):
    global sum
    if (d % 10 == 0):
        sum_single_digit(d / 10)
    elif (d % 10 == d):
        sum = sum + d
        return sum
    else:
        sum = sum + d % 10
        sum_single_digit(d / 10)


def getsum(d):
    total = 0
    d = int(d)
    global sum
    for i in xrange(1, d + 1):
        sum = 0
        sum_single_digit(i)
        total = total + sum
    return total


print getsum("BMC_TEST_INPUT_MAGIC")
#print getsum("12")
