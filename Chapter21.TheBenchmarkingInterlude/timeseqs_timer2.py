#!/usr/bin/env python3
#encoding=utf-8


#------------------------------------------------------------
# Usage: python3 timeseqs_timer2.py
# Description: timer test for multiple implementation
#------------------------------------------------------------


import sys, timer2


reps = 10000
repslist = list(range(reps))


def for_loop():
    res = []
    for x in repslist:
        res.append(x + 10)
    return res


def list_comp():
    return [x + 10 for x in repslist]


def map_call():
    return list(map((lambda x: x + 10), repslist))


def gen_expr():
    return list(x + 10 for x in repslist)


def gen_func():
    def gen():
        for x in repslist:
            yield x + 10
    return list(gen())


print(sys.version)

for test in (for_loop, list_comp, map_call, gen_expr, gen_func):
    (total, result) = timer2.bestoftotal(test, _reps1=5, _reps=1000)
    print('%-9s: %.5f => [%s...%s]' % (test.__name__, total, result[0], result[-1]))



'''
执行结果如下所示：
3.8.6 (default, Nov  9 2020, 16:14:32) 
[GCC 8.3.1 20191121 (Red Hat 8.3.1-5)]
for_loop : 1.24534 => [10...10009]
list_comp: 0.74031 => [10...10009]
map_call : 1.47962 => [10...10009]
gen_expr : 1.01760 => [10...10009]
gen_func : 1.01254 => [10...10009]
'''
