#!/usr/bin/env python3
#encoding=utf-8



#-----------------------------------------
#
#-----------------------------------------


def intersect(seq1, seq2):
    res = []
    for x in seq1:
        if x in seq2:
            res.append(x)
    return res



s1 = 'SPAM'
s2 = 'SCAM'

call_result = intersect(s1, s2)
print('The result of s1 intersect s2 in function call is %s' % call_result)


# The same effect, but more simpler
comp_result = [x for x in s1 if x in s2]
print('The reuslt of s1 intersect s2 in list comprehension is %s' % comp_result)
