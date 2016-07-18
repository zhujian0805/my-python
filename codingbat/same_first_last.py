#!/usr/bin/python
def same_first_last(nums):
    l = len(nums)
    if l >=1:
        if nums[0] == nums[-1]:
            return True
        else:
            return False
    else:
        return False

print same_first_last([1,2,3,4,5,1])
