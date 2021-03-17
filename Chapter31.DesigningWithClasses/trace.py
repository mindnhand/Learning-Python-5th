#!/usr/bin/env python3
#encoding=utf-8


#--------------------------------------------------
# Usage: python3 trace.py
# Description: Delegation, wrapped, proxy
#--------------------------------------------------


class Wrapper:
    def __init__(self, object):
        self.wrapped = object               # Save object
    def __getattr__(self, attrname):
        print('Trace: ' + attrname)         # Trace fetch
        return getattr(self.wrapped, attrname)      # Delegate fetch



if __name__ == '__main__':
    x = Wrapper([1, 2, 3])                  # Wrap a list
    xa = x.append(4)                        # Delegated to list method, will return None
    xv = x.wrapped                          # Print my member
    print(xv)
    print(xa)                               # print None

    y = Wrapper({'a': 1, 'b': 2})           # Wrap a dictionary
    yv = y.keys()
    print(list(yv))                          # Delegate to dictionary method

    '''
    result:
    [root@localhost Chapter31.DesigningWithClasses]# python3 trace.py
    Trace: append
    [1, 2, 3, 4]
    Trace: keys
    ['a', 'b']
    '''
