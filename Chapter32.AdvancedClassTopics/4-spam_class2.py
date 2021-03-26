#!/usr/bin/env python3
#encoding=utf-8


#---------------------------------------------
# Usage: python3 4-spam_class2.py
# Description: Code that needs to manage per-class instance counters, for example,
#              might be best off leveraging class methods. In the following, the 
#              top-level superclass uses a class method to manage state information 
#              that varies for and is stored on each class in the tree -- similar in
#              spirit to the way instance methods manage state information that 
#              varies per class instance
#---------------------------------------------


class SpamClass:
    instance_counter = 0
    def count(cls):                         # per-class instance counter
        cls.instance_counter += 1           # cls is the lowest class above instance
    def __init__(self):
        self.count()                        # pass self.__class__ to count
    count = classmethod(count)

    # @classmethod
    # def count1(cls):
    #     cls.instance_counter += 1


class SpamSub(SpamClass):
    instance_counter = 0
    def __init__(self):                     # Redefine __init__ operator
        SpamClass.__init__(self)


class SpamSubOther(SpamClass):
    instance_counter = 0                    # Inherits __init__ operator



if __name__ == '__main__':
    a = SpamClass()
    b1, b2 = SpamSub(), SpamSub()
    c1, c2, c3 = SpamSubOther(), SpamSubOther(), SpamSubOther()

    print(SpamClass.instance_counter, SpamSub.instance_counter, SpamSubOther.instance_counter)
