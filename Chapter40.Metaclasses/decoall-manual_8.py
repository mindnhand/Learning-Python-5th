#!/usr/bin/env python3
#encoding=utf-8


#---------------------------------------------
# Usage: python3 decoall-manual_8.py
# Description: use decorator manually
#---------------------------------------------


from decotools_8 import tracer


class Person:
    @tracer
    def __init__(self, name, pay):
        self.name = name
        self.pay = pay

    @tracer
    def giveRaise(self, percent):               # giveRaise = tracer(giveRaiser)
        self.pay *= (1.0 + percent)             # onCall remembers giveRaise

    @tracer
    def lastName(self):                         # lastName = tracer(lastName)
        return self.name.split()[-1]



if __name__ == '__main__':
    bob = Person('Bob Smith', 50000)
    sue = Person('Sue Jones', 100000)
    print(bob.name, sue.name)
    sue.giveRaise(.10)                          # runs onCall(sue, .10)
    print('%.2f' % sue.pay)
    print(bob.lastName(), sue.lastName())       # runs onCall(bob), remembers lastName
