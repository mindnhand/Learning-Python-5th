#!/usr/bin/env python3
#encoding=utf-8


#---------------------------------------------
# Usage: python3 converters.py
# Description: compostion and inheritance
#---------------------------------------------



from streams import Processor



class Uppercase(Processor):
    def converter(self, data):
        return data.upper()
'''
Here, the Uppercase class inherits the stream-processing loop logic (and anything else
that may be coded in its superclasses). It needs to define only what is unique about it
—the data conversion logic. When this file is run, it makes and runs an instance that
reads from the file trispam.txt and writes the uppercase equivalent of that file to the
stdout stream:
    c:\code> type trispam.txt
    spam
    Spam
    SPAM!
'''

class HTMLize:
    def write(self, line):
        print('<PRE>%s</PRE>' % line.rstrip())
'''
But, as suggested earlier, we could also pass in arbitrary objects coded as classes that
define the required input and output method interfaces. Here's a simple example that
passes in a writer class that wraps up the text inside HTML tags:
'''

'''
If you trace through this example's control flow, you'll see that we get both uppercase
conversion (by inheritance) and HTML formatting (by composition), even though the
core processing logic in the original Processor superclass knows nothing about either
step. The processing code only cares that writers have a write method and that a method
named convert is defined; it doesn't care what those methods do when they are called.
Such polymorphism and encapsulation of logic is behind much of the power of classes
in Python.
'''

'''
For another example of composition at work, see exercise 9 at the end of Chapter 32
and its solution in Appendix D; it's similar to the pizza shop example. We've focused
on inheritance in this book because that is the main tool that the Python language itself
provides for OOP. But, in practice, composition may be used as much as inheritance
as a way to structure classes, especially in larger systems. As we've seen, inheritance
and composition are often complementary (and sometimes alternative) techniques.
'''

if __name__ == '__main__':
    import sys
    obj = Uppercase(open('trispam.txt'), sys.stdout)
    obj.process()
    # print to file
    prog = Uppercase(open('trispam.txt'), open('trispamup.txt', 'w'))
    prog.process()

    htmlize = Uppercase(open('trispam.txt'), HTMLize())
    htmlize.process()
