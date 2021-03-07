#!/usr/bin/env python3
#encoding=utf-8


#-------------------------------------------------
# Usage: python3 timeseqs.py
# Description: the usage of time module
#-------------------------------------------------



'''
Test the relative speed of iteration tool alternatives
'''

import sys, timer



reps = 10000
repslist = list(range(reps))


def for_loop():
    res = []
    for x in repslist:
        res.append(abs(x))
    return res


def list_comp():
    return [abs(x) for x in repslist]


def map_call():
    return list(map(abs, repslist))
  # return map(abs, repslist)


def gen_expr():
    return list(abs(x) for x in repslist)


def gen_func():
    def gen():
        for x in repslist:
            yield abs(x)
    return list(gen())



print(sys.version)

for test in (for_loop, list_comp, map_call, gen_expr, gen_func):
    (bestof, (total, result)) = timer.bestoftotal(5, 1000, test)
    print('%-9s: %.5f => [%s...%s]' % (test.__name__, bestof, result[0], result[-1]))

'''
The Output Results: 
0.0014824867248535156
(0.00011920928955078125, 'SPAM')
bestof time of tb1 = (0.0, 'SPAM')
bestof time of tb2 = 0.0028412342071533203
bestof time of tb3 = (0.00015926361083984375, (0.0001220703125, 'SPAM'))
bestoftotal time of tbt2 = (0.0001590251922607422, (0.00011897087097167969, 'SPAM'))
3.8.6 (default, Nov  9 2020, 16:14:32) 
[GCC 8.3.1 20191121 (Red Hat 8.3.1-5)]
for_loop : 1.14184 => [0...9999]
list_comp: 0.58819 => [0...9999]
map_call : 0.52128 => [0...9999]
gen_expr : 0.84307 => [0...9999]
gen_func : 0.84155 => [0...9999]
'''

