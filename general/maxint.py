#!/usr/bin/python

x = [10, 8, -1, 100, 200, 200 , 200, 35]

max = 0


def getMaxInt(array):
    global max
    for i in array:
        if i > max:
            max = i
    return max


def getRangeOfNum(x, y):
    if x > 9 and x < 100 and y > 9 and y < 100:
        return True
    return False


getMaxInt(x)

print("Max: %d" % max)


print x

x.sort(getRangeOfNum, reverse = True)

print x
