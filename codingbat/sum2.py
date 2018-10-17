#!/usr/bin/python


def sum2(nums):
    l = len(nums)
    if l == 0:
        return 0
    elif l < 2:
        return nums[0]
    else:
        return nums[0] + nums[1]


print sum2([1, 2, 3])
