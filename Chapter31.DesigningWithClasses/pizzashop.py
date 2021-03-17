#!/usr/bin/env python3
#encoding=utf-8


#--------------------------------------------
# Usage: python3 pizzashop.py
# Description: class instance
#--------------------------------------------


from employees import PizzaRobot, Server

class Customer:
    def __init__(self, name):
        self.name = name
    def order(self, server):
        print(self.name, "orders from", server)
    def pay(self, server):
        print(self.name, 'pays for item to', server)


class Oven:
    def bake(self):
        print('oven bakes')


class PizzaShop:
    def __init__(self):
        self.server = Server('Pat')                     # Embed other objects
        self.chef = PizzaRobot('Bob')                   # A robot named bob
        self.oven = Oven()
    def order(self, name):
        customer = Customer(name)                       # Activate other objects
        customer.order(self.server)                     # Customer orders from server
        self.chef.work()
        self.oven.bake()
        customer.pay(self.server)
'''
The PizzaShop class is a container and controller; its constructor makes and embeds
instances of the employee classes we wrote in the prior section, as well as an Oven class
defined here. When this module's self-test code calls the PizzaShop order method, the
embedded objects are asked to carry out their actions in turn. Notice that we make a
new Customer object for each order, and we pass on the embedded Server object to
Customer methods; customers come and go, but the server is part of the pizza shop
composite. Also notice that employees are still involved in an inheritance relationship;
composition and inheritance are complementary tools.

Again, this is mostly just a toy simulation, but the objects and interactions are representative
of composites at work. As a rule of thumb, classes can represent just about any objects and 
relationships you can express in a sentence; just replace nouns with classes (e.g., Oven), 
and verbs with methods (e.g., bake), and you'll have a first cut at a design.
'''



if __name__ == '__main__':
    scene = PizzaShop()                                 # Make the composite
    scene.order('Homer')                                # Simulate Homer's order
    print('...')
    scene.order('Shaggy')                               # Simulate Shaggy's order
