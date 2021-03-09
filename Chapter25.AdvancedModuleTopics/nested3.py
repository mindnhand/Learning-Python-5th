#!/usr/bin/env python3
#encoding=utf-8


#--------------------------------------------
# Usage: python3 nested3.py
# Description: modify other module's variable
#--------------------------------------------



import nested1                      # Get module as a whole


nested1.x = 88                      # OK: change nested1's x

nested1.printer()
