#!/usr/bin/env python3
#encoding=utf-8


#---------------------------------------------------
# Usage: python3 test_dir1_package_imoprt.py
# Description: test for package import
#---------------------------------------------------


import dir1.dir2.mod    # will print 3 lines


import dir1.dir2.mod    # will not print anything
'''
import statements run each directory's initialization file the first time that directory is
traversed, as Python descends the path.
Just like module files, an already imported directory may be passed to reload to force
reexecution of that single item. As shown here, reload accepts a dotted pathname to
reload nested directories and files:
'''

from importlib import reload
reload(dir1.dir2.mod)   # will only print the info in mod.py
reload(dir1)
reload(dir1.dir2)


'''
交互式测试：
In [14]: import os
In [15]: os.chdir('/data/python/python-learning/Learning-Python-5th/Chapter24.ModulePackages')
In [16]: !ls
dir1  gmon.out  test_dir1_package_imoprt.py

In [17]: from dir1.dir2 import mod
dir1 init
dir2 init
in mod.py

In [18]: mod.z
Out[18]: 3

In [19]: from dir1.dir2.mod import z

In [20]: z
Out[20]: 3

In [21]: import dir1.dir2.mod as mod

In [22]: mod.z
Out[22]: 3

In [23]: from dir1.dir2.mod import z as modz

In [24]: modz
Out[24]: 3

In [25]:
'''
