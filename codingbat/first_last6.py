#!/usr/bin/python

def first_last6(nums):
    n = len(nums)
    if n == 1:
        if nums[0] == 6:
            return True
        else:
            return False
    else:
        if nums[0] == 6 or nums[n-1] == 6:
            return True
        else:
            return False


print first_last6([1,2,6])
