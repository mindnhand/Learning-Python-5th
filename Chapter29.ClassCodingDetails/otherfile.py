#!/usr/bin/env python3
#encoding=utf-8


#-----------------------------------------------
# Usage: otherfile.py
# Description: namespace and scope
#-----------------------------------------------



import manynames


x = 66
print(x)                                            # 66: the global here
print(manynames.x)                                  # 11: globals become attributes after imports


manynames.f()                                       # 11: manynames' x, not the one here
manynames.g()                                       # 22: local in other file's function

print(manynames.C.x)                                # 33: attribute of class in other module

I = manynames.C()
print(I.x)                                          # 33: still from class here

I.m()
print(I.x)                                          # 55: now from instance


'''
Notice here how manynames.f() prints the X in manynames, not the X assigned in this file
—scopes are always determined by the position of assignments in your source code
(i.e., lexically) and are never influenced by what imports what or who imports whom.
Also, notice that the instance’s own X is not created until we call I.m()—attributes, like
all variables, spring into existence when assigned, and not before. Normally we create
instance attributes by assigning them in class __init__ constructor methods, but this
isn’t the only option.
'''
