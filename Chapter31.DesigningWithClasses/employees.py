#!/usr/bin/env python3
#encoding=utf-8


#---------------------------------------------------
# Usage: python3 employees.py
# Description: class inheritance
#---------------------------------------------------



'''
The most general class, Employee, provides common behavior such as bumping up salaries
(giveRaise) and printing (__repr__). There are two kinds of employees, and so two 
subclasses of Employee—Chef and Server. Both override the inherited work method to print 
more specific messages. Finally, our pizza robot is modeled by an even more specific 
class—PizzaRobot is a kind of Chef, which is a kind of Employee. In OOP terms, we call 
these relationships "is-a" links: a robot is a chef, which is an employee. Here's the 
employees.py file:
'''


class Employee:
    def __init__(self, name, salary=0):
        self.name = name
        self.salary = salary
    def giveRaise(self, percent):
        self.salary = self.salary * (1 + percent)
    def work(self):
        print(self.name, 'does stuff')
    def __repr__(self):
        return "<Employee: name=%s, salary=%s>" % (self.name, self.salary)



class Chef(Employee):
    def __init__(self, name):
        Employee.__init__(self, name, 50000)
    def work(self):
        print(self.name, 'make food')



class Server(Employee):
    def __init__(self, name):
        Employee.__init__(self, name, 40000)
    def work(self):
        print(self.name, 'interfaces with customer')


class PizzaRobot(Chef):
    def __init__(self, name):
        Chef.__init__(self, name)
    def work(self):
        print(self.name, "make pizza")




if __name__ == '__main__':
    bob = PizzaRobot('bob')                     # Make a robot named bob
    print(bob)                                  # Run inherited __repr__
    bob.work()                                  # Run type-specific action
    bob.giveRaise(0.20)                         # Give bob a 20% rate
    print(bob)
    print()

    for klass in Employee, Chef, Server, PizzaRobot:
        obj = klass(klass.__name__)
        obj.work()
