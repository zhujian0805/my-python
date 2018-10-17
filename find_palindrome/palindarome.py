#!/usr/bin/python

import sys


def is_palindrome(smallstring):

    reverse = smallstring[::-1]

    if smallstring == reverse:

        return 1

    else:

        return 0


def find_pals(bigstring):

    pal_list = []

    for x in range(0, len(bigstring)):

        for y in range(0, len(bigstring)):

            substring = bigstring[x:y + 1]

            if y < x or len(substring) < 2:

                continue

            else:

                if is_palindrome(substring):

                    pal_list.append(substring)

    print len(pal_list), "palindromes found:\n", pal_list, "\n"

    print max(pal_list, key=len), 'is the largest palindrome'


def main():

    word_of_interest = sys.argv[1]

    find_pals(word_of_interest)


if __name__ == "__main__":

    main()
