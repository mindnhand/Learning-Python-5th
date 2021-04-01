#!/usr/bin/env python3
#encoding=utf-8


#---------------------------------------------------
# Usage: python3 4-getattr-delegate.py
# Description: Delegation-based managers
#---------------------------------------------------



class Person:
    def __init__(self, name, job=None, pay=0):
        self.name = name
        self.job = job
        self.pay = pay
    def lastName(self):
        return self.name.split()[-1]
    def giveRaise(self, percent):
        self.pay = int(self.pay * (1 + percent))
    def __repr__(self):
        return '[Person: %s, %s]' % (self.name, self.pay)

class Manager:
    def __init__(self, name, pay):
        self.person = Person(name, 'mgr', pay) 		# Embed a Person object
    def __getattribute__(self, attr):
        print('**', attr)
        person = object.__getattribute__(self, 'person')
        if attr == 'giveRaise':
            return lambda percent: person.giveRaise(percent + 0.1)
        else:
            return getattr(person, attr)
    def __repr__(self):
        person = object.__getattribute__(self, 'person')
        return str(person)



if __name__ == '__main__':
    sue = Person('Sue Jones', job='dev', pay=100000)
    print(sue.lastName())
    sue.giveRaise(.10)
    print(sue)
    tom = Manager('Tom Jones', 50000) 	# Manager.__init__
    print(tom.lastName()) 				# Manager.__getattr__ -> Person.lastName
    tom.giveRaise(.10) 				# Manager.giveRaise -> Person.giveRaise
    print(tom) 				# Manager.__repr__ -> Person.__repr__

