#!/usr/bin/env python3
#encoding=utf-8


#---------------------------------------
# Usage: python3 4-getattr-person.py
# Description: attribute operator overloading to manage attribute
#---------------------------------------


'''
To see how to put these ideas to work, here is the same first example we used for properties
and descriptors in action again, this time implemented with attribute operator overloading 
methods. Because these methods are so generic, we test attribute names here to know when a
managed attribute is being accessed; others are allowed to pass normally
'''

class Person: 			# Portable: 2.X or 3.X
    def __init__(self, name): 			# On [Person()]
        self._name = name 				# Triggers __setattr__!
    def __getattribute__(self, attr):             # On [obj.any]
        print('getattribute: ' + attr)
        if attr == 'name':            # Intercept all names
            attr = '_name'            # Map to internal name
        return object.__getattribute__(self, attr)    # Avoid looping here
    def __setattr__(self, attr, value): 	# On [obj.any = value]
        print('setattr: ' + attr)
        if attr == 'name':
            attr = '_name' 				# Set internal name
        self.__dict__[attr] = value 		# Avoid looping here
    def __delattr__(self, attr): 			# On [del obj.any]
        print('delattr: ' + attr)
        if attr == 'name':
            attr = '_name' 				# Avoid looping here too
        del self.__dict__[attr] 			# but much less common



if __name__ == '__main__':
    print('1. initialize instance bob')
    bob = Person('Bob Smith') 				# bob has a managed attribute

    print('\n2. fetch attribute of bob')
    print(bob.name) 			# Runs __getattr__
    
    print('\n3. assign attribute of bob')
    bob.name = 'Robert Smith' # Runs __setattr__

    print('\n4. fetch attribute of bob')
    print(bob.name)

    print('\n5. delete attribute of bob')
    del bob.name 				# Runs __delattr__

    print()
    print('-'*20)
    print()

    print('\n6. initialize instance sue')
    sue = Person('Sue Jones') # sue inherits property too

    print('\n7. fetch attribute of sue')
    print(sue.name)
    #print(Person.name.__doc__) # No equivalent here
