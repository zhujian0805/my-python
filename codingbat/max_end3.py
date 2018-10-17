#!/usr/bin/python


def max_end3(nums):
    f = nums[0]
    l = nums[-1]
    if f > l:
        return [f, f, f]
    else:
        return [l, l, l]


print max_end3([1, 2, 3])
