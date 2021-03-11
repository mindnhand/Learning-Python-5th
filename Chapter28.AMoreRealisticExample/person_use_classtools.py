#!/usr/bin/env python3
#encoding=utf-8


#-----------------------------------------------------
# Usage: python3 person_use_classtools.py
# Description: Implement a class
#-----------------------------------------------------




from classtools import AttrDisplay                      # Use generic display tools



class Person(AttrDisplay):                              # Mix in a repr at this level
    '''
    Create and process person records
    '''
    def __init__(self, name, job=None, pay=0):          # Constructor takes three arguments, with default value
        self.name = name                                # Fill out fields when created
        self.job = job                                  # self is the new instance object
        self.pay = pay
        
    def lastName(self):                                 # Behavior methods
        return self.name.split()[-1]                    # self is implied subject

    def giveRaise(self, percent):
        self.pay = int(self.pay * (1 + percent))


class Manager(Person):
    '''
    A customized Person with special requirements
    '''
    def __init__(self, name, pay):                                  # Redefine constructor
        Person.__init__(self, name, 'mgr', pay)                     # Run original with 'mgr'
    def giveRaise(self, percent, bonus=.10):                        # Redefine at this level
        Person.giveRaise(self, percent + bonus)                     # Call Person's version



if __name__ == '__main__':
    # add incremental self-test code
    print('{0:<15s} {1:^5s} {2:>10s}'.format('Name', 'Job', 'Pay'))
    print('-' * 15 + ' ' + '-' * 5 + ' ' + '-' * 10)
    bob = Person('Bob Smith')                           # Test the class
    sue = Person('Sue Jones', job='dev', pay=100000)    # Runs __init__ attributes
    print('{0:<15}'.format(bob.name))
    print('{0:<15s} {job:^5s} {pay:>10d}'.format('Sue Jones', job='dev', pay=100000))
    print()

    print('=' * 40)
    print(bob.lastName(), sue.lastName())               # Use the new method
    sue.giveRaise(.10)                                  # instead of hardcoding
    print('Sue\' salary after giveRaise is %s' % sue.pay)
    print()

    print('=' * 40)
    print('After add __repr__ method')
    print(sue)
    print()

    print('After add Manager class')
    tom = Manager('Tom Jones', 50000)                   # Make a Manager: __init__, job name is not needed
    tom.giveRaise(.10)                                  # Run custom version, net effect, it raise 20%
    print('The last name of %s is %s' % (tom.name, tom.lastName()))          # Run inherited method
    print(tom)                                          # Run inherited __str__
    print()

    print('--All three--')
    for obj in (bob, sue, tom):                         # Process objects generically
        obj.giveRaise(.10)                              # Run this object's giveRaise
        print(obj)
