#!/usr/bin/python


def rotate_left3(nums):
    left = nums[:1]
    right = nums[1:]

    return right + left


print rotate_left3([1, 2, 3, 4])
