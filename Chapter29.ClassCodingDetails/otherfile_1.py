#!/usr/bin/env python3
#encoding=utf-8


#------------------------------------------
# Usage:
# Description:
#------------------------------------------


x = 11                                      # Global in module

def g1():
    print(x)                                # 11: Reference global in module


def g2():
    global x
    x = 22                                          



def h1():
    x = 33                                  # Local in function
    def nested():
        print(x)                            # 33:  Reference local in enclosing scope
    nested()


def h2():
    x = 33                                  # Local in function
    print(x)                                # 33: x in h2
    def nested():
        nonlocal x                          # Python3.x statement
        x = 44                              # Change local in enclosing scope
    nested()
    print(x)                                # 44: modified by nested



if __name__ == '__main__':
    print(x)                                # 11: global
    g1()                                    # 11: global scope from g1
    g2()                                    # no output, but change the global x
    h1()                                    # 33: local x in h1, and printed by nested in h1
    h2()                                    # 33,44: for 33 is local x in h2, for 44 is modified by nested in h2
    print(x)                                # 22: Change global in module

