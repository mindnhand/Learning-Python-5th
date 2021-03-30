#!/usr/bin/env python3
#encoding=utf-8


#-----------------------------------------
# Usage: python3 9-patternparse.py
# Description: parse xml file
#-----------------------------------------


import re


text = open('9-mybooks.xml').read()

found = re.findall('<title>(.*)</title>', text)

for title in found: 
    print(title)
