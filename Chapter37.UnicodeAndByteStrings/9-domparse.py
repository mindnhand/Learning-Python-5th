#!/usr/bin/env python3
#encoding=utf-8


#------------------------------------------
# Usage: python3 9-domparse.py
# Description: method2 of parse xml file
#------------------------------------------

from xml.dom.minidom import parse, Node



xmltree = parse('9-mybooks.xml')


for node1 in xmltree.getElementsByTagName('title'):
    for node2 in node1.childNodes:
        if node2.nodeType == Node.TEXT_NODE:
            print(node2.data)
