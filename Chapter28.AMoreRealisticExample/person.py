#!/usr/bin/env python3
#encoding=utf-8


#-----------------------------------------------------
# Usage: python3 person.py
# Description: Implement a class
#-----------------------------------------------------







class Person:                                           # Mix in a repr at this level
    def __init__(self, name, job=None, pay=0):          # Constructor takes three arguments, with default value
        self.name = name                                # Fill out fields when created
        self.job = job                                  # self is the new instance object
        self.pay = pay
        
    def lastName(self):                                 # Behavior methods
        return self.name.split()[-1]                    # self is implied subject

    def giveRaise(self, percent):
        self.pay = int(self.pay * (1 + percent))

    def __repr__(self):                                 # Added method
        return '[Person: %s, %s]' % (self.name, self.pay)   # String to print

    def __str__(self):
        '''
        如果没有定义__str__，那么无论是在命令行中以脚本的方式执行，还是在python或者ipython中以交互式的方式执行，都是只调用
        __repr__方法；如果定义了__str__方法但是没有定义__repr__方法，效果一样。
        但是，如果这两个方法同时定义的时候，在命令行中以脚本的方式执行的时候，程序中的print语句会优先使用__str__方法，而不是
        使用__repr__方法。

        在ipython中交互式执行的效果如下所示：
        In [16]: reload(person)
        Out[16]: <module 'person' from '/data/python/python-learning/Learning-Python-5th/Chapter28.AMoreRealisticExample/person.py'>

        In [17]: sue = person.Person('Susan Maso', 'mgr', 120000)

        In [18]: sue                                # 调用了__repr__方法
        Out[18]: [Person: Susan Maso, 120000]

        In [19]: print(sue)                         # 调用了__str__方法
        Person Information:
                    Name: Susan Maso
                    Job: mgr
                    Pay: 120000

        在命令行中的执行效果如下所示：
	[root@amdhost Chapter28.AMoreRealisticExample]# python3 person.py
        Name             Job         Pay
        --------------- ----- ----------
        Bob Smith
        Sue Jones        dev      100000
        
        ========================================
        Smith Jones
        Sue' salary after giveRaise is 110000
        
        ========================================
        After add __repr__ method
        Person Information:
                Name: Sue Jones
                Job: dev
                Pay: 110000
        '''
        return 'Person Information:\n\tName: %s\n\tJob: %s\n\tPay: %s\n' % (self.name, self.job, self.pay)

class Manager(Person):
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
