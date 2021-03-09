#!/usr/bin/env python3
#encoding=utf-8


#--------------------------------------------
# Usage: python3 nested2.py
# Description: module scope
#--------------------------------------------



from nested1 import x, printer                  # copy names out

x = 88                                          # Change my x only

printer()                                         # nested1's x is still 99, printer() prints nested1.py's x
