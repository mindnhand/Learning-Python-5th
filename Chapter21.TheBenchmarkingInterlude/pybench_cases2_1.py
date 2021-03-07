#!/usr/bin/env python3
#encoding=utf-8


#-------------------------------------------------------
# Usage: python3 pybench_cases2_1.py [-a] or python2 pybench_cases2_1.py [-a]
# Description: test cases for timeit module
#-------------------------------------------------------



'''
pybench_cases2_1.py: Run pybench on a set of pythons and statements.
Select modes by editing this script or using command-line arguments (in
sys.argv): e.g., run a "C:\python27\python pybench_cases2_1.py" to test just
one specific version on stmts, "pybench_cases2_1.py -a" to test all pythons
listed, or a "py −3 pybench_cases2_1.py -a -t" to trace command lines too.
'''


import sys, pybench2



pythons = [                                                 # (ispy3?, path)
        (1, '/usr/local/python3.8.6/bin/python3'),
        (0, '/usr/bin/python2')
        ]

stmts = [                                                   # (number, repeat, stmt)
        # Use function calls: map wins
        (0, 0, '', "[ord(x) for x in 'spam' * 2500]"),                            # Iteration 
        (0, 0, '', "res=[]\nfor x in 'spam' * 2500: \n\tres.append(ord(x))"),     # \n=multistmt
        (0, 0, "def f(x):\n\treturn x", "[f(x) for x in 'spam' * 2500]"),             # \n\t=indent
        (0, 0, "def f(x):\n\treturn x", "res=[]\nfor x in 'spam' * 2500:\n\tres.append(f(x))"),                        # $=list or ""
        # set and dicts
        (0, 0, '', "{x ** 2 for x in range(1000)}"),          # Strings ops
        (0, 0, '', "s=set()\nfor x in range(10000): \n\ts.add(x ** 2)"),
        (0, 0, '', "{x: x ** 2 for x in range(1000)}"),
        (0, 0, '', "d={}\nfor x in range(1000): \n\td[x] = x ** 2"),
        (0, 0, "l = [1, 2, 3, 4, 5]", "for i in range(len(l)):\n\tl[i] += 1"),
        (0, 0, "l = [1, 2, 3, 4, 5]", "i=0\nwhile i<len(l):\n\tl[i] += 1\n\ti += 1"),
        # Pathological: 300k digits
        (1, 1, '', "len(str(2 ** 1000000))")
        ]


tracecmd = '-t' in sys.argv                                 # -t: trace command lines?
pythons = pythons if '-a' in sys.argv else None             # -a: all in list, else one?
pybench2.runner(stmts, pythons, tracecmd)



'''
第一种执行方式的执行结果如下：
# python3 pybench_cases2_1.py
3.8.6 (default, Nov  9 2020, 16:14:32) 
[GCC 8.3.1 20191121 (Red Hat 8.3.1-5)]
0.5638 ["[ord(x) for x in 'spam' * 2500]"]
1.2459 ["res=[]\nfor x in 'spam' * 2500: \n\tres.append(ord(x))"]
1.0122 ["[f(x) for x in 'spam' * 2500]"]
1.5737 ["res=[]\nfor x in 'spam' * 2500:\n\tres.append(f(x))"]
0.3811 ['{x ** 2 for x in range(1000)}']
4.6835 ['s=set()\nfor x in range(10000): \n\ts.add(x ** 2)']
0.3960 ['{x: x ** 2 for x in range(1000)}']
0.4081 ['d={}\nfor x in range(1000): \n\td[x] = x ** 2']
0.0011 ['for i in range(len(l)):\n\tl[i] += 1']
0.0012 ['i=0\nwhile i<len(l):\n\tl[i] += 1\n\ti += 1']
0.8577 ['len(str(2 ** 1000000))']
'''

'''
第二种执行方式的执行结果如下所示：
# python3 pybench_cases2_1.py -a
3.8.6 (default, Nov  9 2020, 16:14:32) 
[GCC 8.3.1 20191121 (Red Hat 8.3.1-5)]
--------------------------------------------------------------------------------
["[ord(x) for x in 'spam' * 2500]"]
/usr/local/python3.8.6/bin/python3
        1000 loops, best of 5: 589 usec per loop
/usr/bin/python2
        1000 loops, best of 5: 333 usec per loop
--------------------------------------------------------------------------------
["res=[]\nfor x in 'spam' * 2500: \n\tres.append(ord(x))"]
/usr/local/python3.8.6/bin/python3
        1000 loops, best of 5: 1.3 msec per loop
/usr/bin/python2
        1000 loops, best of 5: 711 usec per loop
--------------------------------------------------------------------------------
["[f(x) for x in 'spam' * 2500]"]
/usr/local/python3.8.6/bin/python3
        1000 loops, best of 5: 1.07 msec per loop
/usr/bin/python2
        1000 loops, best of 5: 634 usec per loop
--------------------------------------------------------------------------------
["res=[]\nfor x in 'spam' * 2500:\n\tres.append(f(x))"]
/usr/local/python3.8.6/bin/python3
        1000 loops, best of 5: 1.62 msec per loop
/usr/bin/python2
        1000 loops, best of 5: 1.03 msec per loop 
--------------------------------------------------------------------------------                                                                 
['{x ** 2 for x in range(1000)}']
/usr/local/python3.8.6/bin/python3
        1000 loops, best of 5: 371 usec per loop
/usr/bin/python2
        1000 loops, best of 5: 51.8 usec per loop
--------------------------------------------------------------------------------
['s=set()\nfor x in range(10000): \n\ts.add(x ** 2)']
/usr/local/python3.8.6/bin/python3
        1000 loops, best of 5: 4.57 msec per loop
/usr/bin/python2
        1000 loops, best of 5: 1.06 msec per loop
--------------------------------------------------------------------------------
['{x: x ** 2 for x in range(1000)}']
/usr/local/python3.8.6/bin/python3
        1000 loops, best of 5: 401 usec per loop
/usr/bin/python2
        1000 loops, best of 5: 51.9 usec per loop
--------------------------------------------------------------------------------
['d={}\nfor x in range(1000): \n\td[x] = x ** 2']
/usr/local/python3.8.6/bin/python3
        1000 loops, best of 5: 415 usec per loop
/usr/bin/python2
        1000 loops, best of 5: 56.2 usec per loop
--------------------------------------------------------------------------------
['for i in range(len(l)):\n\tl[i] += 1']
/usr/local/python3.8.6/bin/python3
        1000 loops, best of 5: 1.1 usec per loop
/usr/bin/python2
        1000 loops, best of 5: 0.451 usec per loop
--------------------------------------------------------------------------------
['i=0\nwhile i<len(l):\n\tl[i] += 1\n\ti += 1']
/usr/local/python3.8.6/bin/python3
        1000 loops, best of 5: 1.26 usec per loop
/usr/bin/python2
        1000 loops, best of 5: 0.489 usec per loop
--------------------------------------------------------------------------------
['len(str(2 ** 1000000))']
/usr/local/python3.8.6/bin/python3
        1 loop, best of 1: 857 msec per loop
/usr/bin/python2
        1 loops, best of 1: 907 msec per loop
'''
