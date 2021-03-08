#encoding=utf-8
import sys
import os

sys.path.append(os.curdir)

import pkg.spam_1         # python2.7 will work, but python3.x will not


'''
没有pkg/string.py这个文件的时候，执行结果如下：
[root@localhost code]# python3 test_pkg_both_work.py
<module 'string' from '/usr/local/python3.8.6/lib/python3.8/string.py'>
99999
[root@localhost code]# python2 test_pkg_both_work.py
<module 'string' from '/usr/lib64/python2.7/string.pyc'>
99999
[root@localhost code]# 
'''


'''
有pkg/string.py这个文件的时候，执行结果如下所示：
[root@localhost code]# python2 test_pkg_both_work.py
stringstringstringstringstringstringstringstring
<module 'pkg.string' from '/data/python/python-learning/Learning-Python-5th/Chapter24.ModulePackages/code/pkg/string.pyc'>
99999
[root@localhost code]# python3 test_pkg_both_work.py
<module 'string' from '/usr/local/python3.8.6/lib/python3.8/string.py'>
99999
[root@localhost code]# 
从上述结果可以看出，虽然使用的是绝对导入，
但在2.x仍然导入了当前目录的string.py这个模块文件
而在3.x中则是直接导入了系统的标准库string.py模块
'''
