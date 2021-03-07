#!/usr/bin/env python3
#encoding=utf-8


#-------------------------------------------------------
# Usage: python3 pybench_cases.py [-a] or python2 pybench_cases.py [-a]
# Description: test cases for timeit module
#-------------------------------------------------------



'''
pybench_cases.py: Run pybench on a set of pythons and statements.
Select modes by editing this script or using command-line arguments (in
sys.argv): e.g., run a "C:\python27\python pybench_cases.py" to test just
one specific version on stmts, "pybench_cases.py -a" to test all pythons
listed, or a "py −3 pybench_cases.py -a -t" to trace command lines too.
'''


import sys, pybench



pythons = [                                                 # (ispy3?, path)
        (1, '/usr/local/python3.8.6/bin/python3'),
        (0, '/usr/bin/python2')
        ]

stmts = [                                                   # (number, repeat, stmt)
        (0, 0, '[x ** 2 for x in range(1000)]'),                            # Iteration 
        (0, 0, 'res=[]\nfor x in range(1000): \n\tres.append(x ** 2)'),     # \n=multistmt
        (0, 0, '$listif3(map(lambda x: x ** 2, range(1000)))'),             # \n\t=indent
        (0, 0, 'list(x ** 2 for x in range(1000))'),                        # $=list or ''
        (0, 0, "s='spam' * 2500\nx=[s[i] for i in range(10000)]"),          # Strings ops
        (0, 0, "s='?'\nfor i in range(10000): s+='?'")
        ]


tracecmd = '-t' in sys.argv                                 # -t: trace command lines?
pythons = pythons if '-a' in sys.argv else None             # -a: all in list, else one?
pybench.runner(stmts, pythons, tracecmd)



'''
第一种执行方式的执行结果如下：
[root@localhost Chapter21.TheBenchmarkingInterlude]# python3 pybench_cases.py
3.8.6 (default, Nov  9 2020, 16:14:32) 
[GCC 8.3.1 20191121 (Red Hat 8.3.1-5)]
0.3671 ['[x ** 2 for x in range(1000)]']
0.4229 ['res=[]\nfor x in range(1000): \n\tres.append(x ** 2)']
0.4426 ['list(map(lambda x: x ** 2, range(1000)))']
0.3954 ['list(x ** 2 for x in range(1000))']
0.9410 ["s='spam' * 2500\nx=[s[i] for i in range(10000)]"]
1.1485 ["s='?'\nfor i in range(10000): s+='?'"]
[root@localhost Chapter21.TheBenchmarkingInterlude]# python2 pybench_cases.py
2.7.17 (default, Aug 31 2020, 21:02:14) 
[GCC 8.3.1 20191121 (Red Hat 8.3.1-5)]
0.0372 ['[x ** 2 for x in range(1000)]']
0.0698 ['res=[]\nfor x in range(1000): \n\tres.append(x ** 2)']
0.0891 ['(map(lambda x: x ** 2, range(1000)))']
0.0461 ['list(x ** 2 for x in range(1000))']
0.3345 ["s='spam' * 2500\nx=[s[i] for i in range(10000)]"]
0.4464 ["s='?'\nfor i in range(10000): s+='?'"]
'''

'''
[root@amdhost Chapter21.TheBenchmarkingInterlude]# python3 pybench_cases.py -a   
3.8.6 (default, Nov  9 2020, 16:14:32)                                                                    
[GCC 8.3.1 20191121 (Red Hat 8.3.1-5)]
--------------------------------------------------------------------------------       
['[x ** 2 for x in range(1000)]']    
/usr/local/python3.8.6/bin/python3      
        1000 loops, best of 5: 347 usec per loop  
/usr/bin/python2         
        1000 loops, best of 5: 36.4 usec per loop   
--------------------------------------------------------------------------------                                                  
['res=[]\nfor x in range(1000): \n\tres.append(x ** 2)']
/usr/local/python3.8.6/bin/python3
        1000 loops, best of 5: 405 usec per loop
/usr/bin/python2
        1000 loops, best of 5: 67.7 usec per loop
--------------------------------------------------------------------------------
['$listif3(map(lambda x: x ** 2, range(1000)))']
/usr/local/python3.8.6/bin/python3
        1000 loops, best of 5: 430 usec per loop
/usr/bin/python2
        1000 loops, best of 5: 92.4 usec per loop
--------------------------------------------------------------------------------       
['list(x ** 2 for x in range(1000))']
/usr/local/python3.8.6/bin/python3
        1000 loops, best of 5: 380 usec per loop
/usr/bin/python2
        1000 loops, best of 5: 44.6 usec per loop
--------------------------------------------------------------------------------
["s='spam' * 2500\nx=[s[i] for i in range(10000)]"]
/usr/local/python3.8.6/bin/python3
        1000 loops, best of 5: 919 usec per loop
/usr/bin/python2
        1000 loops, best of 5: 332 usec per loop
--------------------------------------------------------------------------------
["s='?'\nfor i in range(10000): s+='?'"]
/usr/local/python3.8.6/bin/python3
        1000 loops, best of 5: 1.1 msec per loop
/usr/bin/python2
        1000 loops, best of 5: 437 usec per loop
'''
