#!/usr/bin/env python3
#encoding=utf-8


#------------------------------------------------
# Usage: python3 simplest_class.py
# Description: class attribute and method
#------------------------------------------------



class Rec:                                          # Empty namespace object
    ...




if __name__ == '__main__':
    Rec.name = 'Bob'                                # Just objects with attributes, class attribute
    Rec.age = 40

    print(Rec.name)                                 # Like a C struct

    x = Rec()                                       # Instances inherit class names
    y = Rec()

    print(x.name)                                   # name is stored on the class only
    print(y.name)

    x.name = 'Sue'                                  # but assignment changes x only
    print(Rec.name, x.name, y.name)
    print()

    print('the dict of Rec class')
    print(list(Rec.__dict__.keys()))
    print()
    print('the dict of Rec class without __xxx__ methods')
    print(list(x for x in Rec.__dict__ if not x.startswith('__')))
    print()
    print('the dict of object x')
    print(list(x.__dict__.keys()))
    print()
    print('the dict of object y')
    print(list(y.__dict__.keys()))
    print()



    '''
    Here, the class's namespace dictionary shows the name and age attributes we assigned
    to it, x has its own name, and y is still empty. Because of this model, an attribute can
    often be fetched by either dictionary indexing or attribute notation, but only if it's
    present on the object in question—attribute notation kicks off inheritance search, but
    indexing looks in the single object only (as we'll see later, both have valid roles):
    '''
    print('the difference between attribute notation and dictionary indexing')
    print('the name of x is ', x.name, x.__dict__['name'])
    print('the age of x by attribute notation is %s' % x.age)                       # But attribute fetch checks classes too
    # print('the age of x by dictionary indexing is %s' % x.__dict__['age'])
    try:
        print('the age of x by dictionary indexing is %s' % x.__dict__['age'])      # Indexing dict does not do inherientance
    except Exception as e:
        print('x has not age key in x.__dict__')

    '''
    To facilitate inheritance search on attribute fetches, each instance has a link to its class
    that Python creates for us—itt's called __class__, if you want to inspect it:
    '''
    print()
    print('x.__class__ is %s' % str(x.__class__))



    '''
    Classes also have a __bases__ attribute, which is a tuple of references to their superclass
    objects—in this example just the implied object root class in Python 3.X wee'll explore
    later (you'll get an empty tuple in 2.X instead):
    '''
    print()
    print('The __bases__ of Rec class is %s' % Rec.__bases__)


    '''
    Even methods, normally created by a def nested in a class, can be created completely
    independently of any class object. The following, for example, defines a simple function
    outside of any class that takes one argument:
    '''
    def uppername(obj):
        return obj.name.upper()                         # Still needs a self argument (obj)

    '''
    There is nothing about a class here yet—itt's a simple function, and it can be called as
    such at this point, provided we pass in an object obj with a name attribute, whose value
    in turn has an upper method—our class instances happen to fit the expected interface,
    and kick off string uppercase conversion:
    '''
    print()
    print('the uppercase name of x is ', uppername(x))


    '''
    If we assign this simple function to an attribute of our class, though, it becomes a
    method, callable through any instance, as well as through the class name itself as long
    as we pass in an instance manually
    '''
    Rec.method = uppername                              # Now it's a class's method!
    print('after add uppername method to Rec class')
    print('the uppercase name of x with x.method is ', x.method())      # Run method to process x
    print('the uppercase name of y with y.method is ', y.method())      # The same, but pass y to self
    print('the uppercase name of x with Rec.method(x) is ', y.method())      # Can call through instance or class
