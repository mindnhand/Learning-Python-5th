#!/usr/bin/env python3
#encoding=utf-8


#-----------------------------------------------------------
# Usage: python3 timeseqs2.py
# Description: time module with different implementation
#-----------------------------------------------------------



import sys, timer


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
    (bestof, (total, result)) = timer.bestoftotal(5, 1000, test)
    print('%-9s: %.5f => [%s...%s]' % (test.__name__, bestof, result[0], result[-1]))

'''
执行结果如下：
0.0017566680908203125
(0.00012350082397460938, 'SPAM')
bestof time of tb1 = (0.0, 'SPAM')
bestof time of tb2 = 0.0029191970825195312
bestof time of tb3 = (0.00016379356384277344, (0.00012254714965820312, 'SPAM'))
bestoftotal time of tbt2 = (0.00016427040100097656, (0.0001232624053955078, 'SPAM'))
3.8.6 (default, Nov  9 2020, 16:14:32) 
[GCC 8.3.1 20191121 (Red Hat 8.3.1-5)]
for_loop : 1.32099 => [10...10009]
list_comp: 0.73948 => [10...10009]
map_call : 1.51109 => [10...10009]
gen_expr : 1.03686 => [10...10009]
gen_func : 1.03553 => [10...10009]
'''
