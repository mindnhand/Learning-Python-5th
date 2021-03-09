#!/usr/bin/env python3
#encoding=utf-8


#---------------------------------------------------
# Usage: python3 runme.py
# Description: __name__ attribute and __main__ module
#---------------------------------------------------


'''
each module has a built-in attribute called __name__, which
Python creates and assigns automatically as follows:
    • If the file is being run as a top-level program file, __name__ is set to the string
    "__main__" when it starts.
    • If the file is being imported instead, __name__ is set to the modulee's name as known
    by its clients.
The upshot is that a module can test its own __name__ to determine whether it's being
run or imported. For example, suppose we create the following module file, named
runme.py, to export a single function called tester:
'''


def tester():
    print("It's Christmas in Heaven...")



if __name__ == '__main__':                      # Only when run
    tester()                                    # Not when imported
    '''
    For instance, perhaps the most common way you'l see the __name__ test applied is for
    self-test code. In short, you can package code that tests a module’s exports in the module
    itself by wrapping it in a __name__ test at the bottom of the file. This way, you can use
    the file in clients by importing it, but also test its logic by running it from the system
    shell or via another launching scheme.
    '''



'''
在命令执行的时候，才会执行if语句中的函数调用；
[root@localhost Chapter25.AdvancedModuleTopics]# python3 runme.py
It's Christmas in Heaven...
在交互式执行的时候，只导入该模块，不调用函数：
In [93]: import runme

In [94]: runme.tester()
It's Christmas in Heaven...
'''
