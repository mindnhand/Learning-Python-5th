#!/usr/bin/env python3
#encoding=utf-8


#------------------------------------------------------
# Usage: python3 method_examples.py
# Description: method example: call class method and instance method
#------------------------------------------------------



class NextClass:                                        # Define class
    def printer(self, text):                            # Define method
        self.message = text                             # Change instance
        print(self.message)



'''
The name printer references a function object; because it's assigned in the class statement's
scope, it becomes a class object attribute and is inherited by every instance made
from the class. Normally, because methods like printer are designed to process instances,
we call them through instances:
'''
x = NextClass()                                         # Make instance
x.printer('x.printer is instance call')                 # Call its method
print('x.message is <%s>' % x.message)


'''
When we call the method by qualifying an instance like this, printer is first located by
inheritance, and then its self argument is automatically assigned the instance object
(x); the text argument gets the string passed at the call ('instance call'). Notice that
because Python automatically passes the first argument to self for us, we only actually
have to pass in one argument. Inside printer, the name self is used to access or set
per-instance data because it refers back to the instance currently being processed.
As we’ve seen, though, methods may be called in one of two ways—through an instance,
or through the class itself. For example, we can also call printer by going
through the class name, provided we pass an instance to the self argument explicitly:
'''
NextClass.printer(x, 'NextClass.printer is class call') # Direct class call
print(x.message)                                        # Instance changed again


'''
Calls routed through the instance and the class have the exact same effect, as long as
we pass the same instance object ourselves in the class form. By default, in fact, you get
an error message if you try to call a method without any instance:
    >>> NextClass.printer('bad call')
    TypeError: unbound method printer() must be called with NextClass instance...
'''
