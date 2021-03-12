#!/usr/bin/env python3
#encoding=utf-8


#---------------------------------------------------
# Usage: python3 shared_attr.py
# Description: class attributes
#---------------------------------------------------



'''
Because class is a compound statement, any sort of statement can be nested inside its
body—print, assignments, if, def, and so on. All the statements inside the class statement
run when the class statement itself runs (not when the class is later called to make
an instance). Typically, assignment statements inside the class statement make data
attributes, and nested defs make method attributes. In general, though, any type of
name assignment at the top level of a class statement creates a same-named attribute
of the resulting class object.
For example, assignments of simple nonfunction objects to class attributes produce
data attributes, shared by all instances:
'''


class SharedData:
    spam = 42                                                   # Generates a class data attribute




if __name__ == '__main__':
    x = SharedData()                                            # Make two instances
    y = SharedData()

    print('x.spam = %s\ty.spam = %s' % (x.spam, y.spam))        # They inherite and share 'spam'(A.K.A SharedData.spam)
    print()

    print('==After modify SharedData.spam==')
    SharedData.spam = 99
    '''
    Here, because the name spam is assigned at the top level of a class statement, it is
    attached to the class and so will be shared by all instances. We can change it by going
    through the class name, and we can refer to it through either instances or the class:1
    '''
    print('x.spam = %s\ty.spam = %s\tSharedData.spam = %s' % (x.spam, y.spam, SharedData.spam))
    print()

    print('==After modify x.spam==')
    x.spam = 88
    '''
    Such class attributes can be used to manage information that spans all the instances—
    a counter of the number of instances generated, for example (we'll expand on this idea
    by example in Chapter 32).
    Modify instance attributes will not change other instance attributes or class attributes:
    '''
    print('x.spam = %s\ty.spam = %s\tSharedData.spam = %s' % (x.spam, y.spam, SharedData.spam))
    print()
    


    '''
    Assignments to instance attributes create or change the names in the instance, rather
    than in the shared class. More generally, inheritance searches occur only on attribute
    references, not on assignment: assigning to an object's attribute always changes that
    object, and no other.2 For example, y.spam is looked up in the class by inheritance, but
    the assignment to x.spam attaches a name to x itself.
    Here's a more comprehensive example of this behavior that stores the same name in
    two places. Suppose we run the following class:
    '''
    class MixedNames:                                   # Define class
        data = 'spam'                                   # Assign class attr
        def __init__(self, value):                      # Assign method name
            self.data = value                           # Assign instance attr

        def display(self):
            print(self.data, MixedNames.data)           # Instance attr, class attr

    '''
    This class contains two defs, which bind class attributes to method functions. It also
    contains an = assignment statement; because this assignment assigns the name data
    inside the class, it lives in the class's local scope and becomes an attribute of the class
    object. Like all class attributes, this data is inherited and shared by all instances of the
    class that don't have data attributes of their own.
    When we make instances of this class, the name data is attached to those instances by
    the assignment to self.data in the constructor method:
    '''
    x = MixedNames(1)                                   # Make two instance objects
    y = MixedNames(2)                                   # Each has its own data
    x.display(), y.display()                            # self.data differs, MixedNames.data is the same
    '''
    The net result is that data lives in two places: in the instance objects (created by the
    self.data assignment in __init__), and in the class from which they inherit names
    (created by the data assignment in the class). The class’s display method prints both
    versions, by first qualifying the self instance, and then the class.
    By using these techniques to store attributes in different objects, we determine their
    scope of visibility. When attached to classes, names are shared; in instances, names
    record per-instance data, not shared behavior or data. Although inheritance searches
    look up names for us, we can always get to an attribute anywhere in a tree by accessing
    the desired object directly.
    In the preceding example, for instance, specifying x.data or self.data will return an
    instance name, which normally hides the same name in the class; however, Mixed
    Names.data grabs the class's version of the name explicitly. The next section describes
    one of the most common roles for such coding patterns, and explains more about the
    way we deployed it in the prior chapter.
    '''

