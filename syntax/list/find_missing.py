#!/usr/bin/python
import re


def findit(l1, l2):
    ll = []
    for i2 in l2:
        count = 0
        for i1 in l1:
            if re.search(i1, i2):
                count = count + 1
        if count == 0:
            ll.append(i2)
    return ll


def main():
    l1 = ['a', 'b']
    l2 = ['fuck', 'abc', 'eeee']

    missing = findit(l1, l2)

    print missing


if __name__ == "__main__":
    main()
