#!/usr/bin/env python3 
#encoding=utf-8


#----------------------------------------------
# Usage: python3 private0.py
# Description: attribute access: Emulating Privacy for Instance Attributes: Part 1 
#----------------------------------------------



'''
As another use case for such tools, the following code—file private0.py—generalizes
the previous example, to allow each subclass to have its own list of private names that
cannot be assigned to its instances (and uses a user-defined exception class, which you'll
have to take on faith until Part VII):
'''


class PrivateExc(Exception):                                        # More on exceptions in Part VII
    pass


class Privacy:
    def __setattr__(self, attrname, value):                         # On self.attrname = value
        if attrname in self.privates:
            raise PrivateExc(attrname, self)                        # Make, raise user-define except
        else:
            self.__dict__[attrname] = value                         # Avoid loops by using dict key


class Test1(Privacy):
    privates = ['age']


class Test2(Privacy):
    privates = ['name', 'pay']
    def __init__(self):
        self.__dict__['name'] = 'Tom'                               # To do better, see Chapter 39!




if __name__ == '__main__':
    x = Test1()
    y = Test2()

    x.name = 'Bob'                          # Works
   #y.name = 'Sue'                          # Fails
    print(x.name)

    y.age = 30                              # Works
   #x.age = 40                              # Fails
    print(y.age)


    '''
    In fact, this is a first-cut solution for an implementation of attribute privacy in Python
    —disallowing changes to attribute names outside a class. Although Python doesnn't
    support private declarations per se, techniques like this can emulate much of their
    purpose.
    This is a partial—and even clumsy—solution, though; to make it more effective, we
    must augment it to allow classes to set their private attributes more naturally, without
    having to go through __dict__ each time, as the constructor must do here to avoid
    triggering __setattr__ and an exception. A better and more complete approach might
    require a wrapper ("proxy") class to check for private attribute accesses made outside
    the class only, and a __getattr__ to validate attribute fetches too.
    We'll postpone a more complete solution to attribute privacy until Chapter 39, where
    we'll use class decorators to intercept and validate attributes more generally. Even
    though privacy can be emulated this way, though, it almost never is in practice. Python
    programmers are able to write large OOP frameworks and applications without private
    declarations—an interesting finding about access controls in general that is beyond the
    scope of our purposes here.
    Still, catching attribute references and assignments is generally a useful technique; it
    supports delegation, a design technique that allows controller objects to wrap up embedded
    objects, add new behaviors, and route other operations back to the wrapped
    objects. Because they involve design topics, we'll revisit delegation and wrapper classes
    in the next chapter.
    '''
