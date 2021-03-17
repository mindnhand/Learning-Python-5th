#!/usr/bin/env python3
#encoding=utf-8


#-------------------------------------------------
# Usage: python3 streams.py
# Description: composition and inheritance
#-------------------------------------------------



'''
Rather than using a simple function here, we might code this as a class that uses 
composition to do its work in order to provide more structure and support inheritance. 
The following 3.X/2.X file, streams.py, demonstrates one way to code the class:
'''


class Processor:
    def __init__(self, reader, writer):
        self.reader = reader
        self.writer = writer
    def process(self):
        while True:
            data = self.reader.readline()
            if not data: break
            data = self.converter(data)
            self.writer.write(data)
    def converter(self, data):
        assert False, 'Converter must be defined'               # Or raise exception
    '''
    This class defines a converter method that it expects subclasses to fill in; it's an example
    of the abstract superclass model we outlined in Chapter 29 (more on assert in Part VII—
    it simply raises an exception if its test is false). Coded this way, reader and writer objects
    are embedded within the class instance (composition), and we supply the conversion logic in a 
    subclass rather than passing in a converter function (inheritance). The file converters.py
    '''
