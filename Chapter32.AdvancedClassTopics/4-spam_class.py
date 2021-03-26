#!/usr/bin/env python3
#encoding=utf-8


#---------------------------------------
# Usage: python3 4-spam_class.py
# Description: Rather than hardcoding the class name, the class method uses 
#              the automatically passed class object generically
#---------------------------------------



class SpamClass:
    instance_counter = 0
    def __init__(self):
        SpamClass.instance_counter += 1

    @classmethod
    def print_instance_counter(cls):
        print('Number of instances: %s %s' % (cls.instance_counter, cls))

    def print_instance_counter1(cls):
        print('Number of instances: %s %s' % (cls.instance_counter, cls))
    print_instance_counter1 = classmethod(print_instance_counter1)

'''
When using class methods, though, keep in mind that they receive the most specific 
(i.e., lowest) class of the call's subject. This has some subtle implications when 
trying to update class data through the passed-in class. For example, if in module 
spam_class.py we subclass to customize as before, augment Spam.printNumInstances to
also display its cls argument, and start a new testing session
'''
class SpamClassSub(SpamClass):
    @classmethod
    def print_instance_counter(cls):               # overwrite class method
        print('Extra stuff...', cls)
        SpamClass.print_instance_counter()      # but call back original method

    def print_instance_counter1(cls):              # overwrite class method
        print('Extra stuff...', cls)
        SpamClass.print_instance_counter1()     # but call back original method
    print_instance_counter1 = classmethod(print_instance_counter1)


class SpamClassSubOther(SpamClass):
    pass



if __name__ == '__main__':
    print('SpamClass classmethod')
    a1 = SpamClass()
    a2 = SpamClass()
    a3 = SpamClass()

    SpamClass.print_instance_counter()
    SpamClass.print_instance_counter1()
    a3.print_instance_counter1()
    print()

    print('Subclass of SpamClass: SpamClassSub')
    sa1 = SpamClassSub()
    sa2 = SpamClassSub()
    sa3 = SpamClassSub()

    SpamClassSub.print_instance_counter()
    SpamClassSub.print_instance_counter1()
    sa3.print_instance_counter1()
    print()

    print('Subclass of SpamClass: SpamClassSubOther')
    sao1 = SpamClassSubOther()
    sao2 = SpamClassSubOther()
    sao3 = SpamClassSubOther()

    SpamClassSubOther.print_instance_counter()
    SpamClassSubOther.print_instance_counter1()
    sao3.print_instance_counter1()
    print()

    '''
    This last call here passes Other to Spam's class method. This works in this example
    because fetching the counter finds it in Spam by inherita nce. If this method tried
    to assign to the passed class's data, though, it would update Other, not Spam! In this
    specific case, Spam is probably better off hardcoding its own class name to update its
    data if it means to count instances of all its subclasses too, rather than relying on 
    the passed-in class argument.
    '''

    '''
    results:
    Chapter32.AdvancedClassTopics]# python3 4-spam_class.py
    SpamClass classmethod
    Number of instances: 3 <class '__main__.SpamClass'>
    Number of instances: 3 <class '__main__.SpamClass'>
    Number of instances: 3 <class '__main__.SpamClass'>

    Subclass of SpamClass: SpamClassSub
    Extra stuff... <class '__main__.SpamClassSub'>
    Number of instances: 6 <class '__main__.SpamClass'>
    Extra stuff... <class '__main__.SpamClassSub'>
    Number of instances: 6 <class '__main__.SpamClass'>
    Extra stuff... <class '__main__.SpamClassSub'>
    Number of instances: 6 <class '__main__.SpamClass'>

    Subclass of SpamClass: SpamClassSubOther
    Number of instances: 9 <class '__main__.SpamClassSubOther'>
    Number of instances: 9 <class '__main__.SpamClassSubOther'>
    Number of instances: 9 <class '__main__.SpamClassSubOther'>
    '''
