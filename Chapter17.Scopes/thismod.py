#!/usr/bin/env python3
#encoding=utf-8


#-----------------------------------
# Usage: 
#    1. in command line:
#         Chapter17.Scopes]# python3 thismod.py                                                                                             
#         before modification, var = 99
#         in globe2 thismod.var, before modification, thismod.var = 99
#         in glob2 thismod.var = 100
#         in glob3 sys.modules.var, before modification, sys.modules.var = 100
#         in glob3 sys.modules.var = 101
#         after call local, glob1, glob2, glob3, var = 100
#    2. in ipython:
#         In [22]: os.chdir('/data/python/python-learning/Learning-Python-5th/Chapter17.Scopes')
#         In [23]: import thismod
#         In [24]: thismod.test()
#         before modification, var = 99
#         in globe2 thismod.var, before modification, thismod.var = 100
#         in glob2 thismod.var = 101
#         in glob3 sys.modules.var, before modification, sys.modules.var = 101
#         in glob3 sys.modules.var = 102
#         after call local, glob1, glob2, glob3, var = 102
# Description: 两种运行方式的最终结果不一样，
#              在命令行中执行，var的最终结果为100，
#              在ipython中执行，var的最终结果为102。
#-----------------------------------



var = 99


def local():
    var = 0                             # Change local var


def glob1():
    global var                          # Declare global (normal)
    var += 1                            # Change global var, after call this function, global var=100

def glob2():
    var = 0                             # Change local var
    import thismod                      # import myself
    print('in globe2 thismod.var, before modification, thismod.var = %s' % thismod.var)
    thismod.var += 1                    # change global var
    print('in glob2 thismod.var = %s' % thismod.var) # 101

def glob3():
    var = 0                             # Change local var
    import sys                          # import sys module
    glob = sys.modules['thismod']       # Get module object(or use __name__)
    print('in glob3 sys.modules.var, before modification, sys.modules.var = %s' % glob.var)
    glob.var += 1                       # Change global var
    print('in glob3 sys.modules.var = %s' % glob.var) # 102

def test():
    print('before modification, var = %s' % var)    # print global var 99
    local(); glob1(); glob2(); glob3()
    print('after call local, glob1, glob2, glob3, var = %s' % var)      # print global var

if __name__ == '__main__':
    test()
