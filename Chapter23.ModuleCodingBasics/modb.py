#!/usr/bin/env python3
#encoding=utf-8


#-------------------------------------------------------
# Usage: python3 modb.py
# Description: module basic and scope
#-------------------------------------------------------



x = 11              # x, global to this file only


import moda         # Gain access to names in moda

moda.f()            # Sets moda.x, not this file's x

print(x, moda.x)    # print 11 99
