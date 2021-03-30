#!/usr/bin/env python3
#encoding=utf-8


#-----------------------------------------------
# Usage: python3 9-saxparse.py
# Description: method3 for parsing xml file
#-----------------------------------------------


import xml.sax
import xml.sax.handler


class BookHandler(xml.sax.handler.ContentHandler):
    def __init__(self):
        self.inTitle = False
    def startElement(self, name, attributes):
        if name == 'title':
            self.inTitle = True
    def characters(self, data):
        if self.inTitle:
            print(data)
    def endElement(self, name):
        if name == 'title':
            self.inTitle = False



if __name__ == '__main__':
    parser = xml.sax.make_parser()
    handler = BookHandler()
    parser.setContentHandler(handler)
    parser.parse('9-mybooks.xml')
