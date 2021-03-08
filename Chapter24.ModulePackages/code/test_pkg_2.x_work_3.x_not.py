import sys
import os

sys.path.append(os.curdir)

import pkg.spam         # python2.7 will work, but python3.x will not


'''
[root@localhost code]# python2 test_pkg.py
<module 'string' from '/usr/lib64/python2.7/string.pyc'>
99999
[root@localhost code]# python test_pkg.py
Traceback (most recent call last):
  File "test_pkg.py", line 6, in <module>
    import pkg.spam
  File "/data/python/python-learning/Learning-Python-5th/Chapter24.ModulePackages/code/pkg/spam.py", line 1, in <module>
    import eggs
ModuleNotFoundError: No module named 'eggs'
[root@localhost code]# python --version
Python 3.8.6
[root@localhost code]#
'''
