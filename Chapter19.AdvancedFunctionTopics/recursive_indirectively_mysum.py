#!/usr/bin/env python3
#encoding=utf-8


#-------------------------------------------
# Usage: python3 recursive_indirectively_mysum.py
# Description: indirectively recursive call
#-------------------------------------------



def mysum(seq):
    if not seq:
        return 0
    return nonempty(seq)


def nonempty(seq):
    return seq[0] + mysum(seq[1:])


#------------------test--------------------
seq_tup = (1, 2, 3, 4, 5)

sum_res = mysum(seq_tup)
print('the sum of %s is %s' % (seq_tup, sum_res))
