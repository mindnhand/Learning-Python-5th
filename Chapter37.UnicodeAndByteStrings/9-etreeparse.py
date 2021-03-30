#!/usr/bin/env python3
#encoding=utf-8


#-------------------------------------
# Usage: python3 9-etreeparse.py
# Description: method4 for parsing xml file
#-------------------------------------



from xml.etree.ElementTree import parse


tree = parse('9-mybooks.xml')

for E in tree.findall('title'):
    print(E.text)
