#!/usr/bin/python

def array_count9(nums):
    count = 0
    for n in nums:
        if n == 9:
            count = count + 1
    return count


print array_count9([1,2,3,9,6,9,9])
