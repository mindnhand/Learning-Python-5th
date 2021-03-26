#!/usr/bin/env python3
#encoding=utf-8


#--------------------------------------
# Usage: python3 4-spam_special.py
# Description: here is the static method equivalent of this section's instance-counting example
#--------------------------------------


class SpamStatic:
    instance_counter = 0
    def __init__(self):
        SpamStatic.instance_counter += 1
    @staticmethod
    def print_instance_counter():
        print('Number of instances: %s' % SpamStatic.instance_counter)

    def print_instance_counter1():
        print('Number of instances: %s' % SpamStatic.instance_counter)
    print_instance_counter1 = staticmethod(print_instance_counter1)



class SpamSub(SpamStatic):
    @staticmethod
    def print_instance_counter():           # overwirte static method
        print('Extra stuff...')
        SpamStatic.print_instance_counter()     # but call the original static method

    def print_instance_counter1():
        print('Extra stuff...')
        SpamStatic.print_instance_counter1()
    print_instance_counter1 = staticmethod(print_instance_counter1)


class SpamSubOther(SpamStatic):
    pass



if __name__ == '__main__':
    print('SpamStatic class')
    a1 = SpamStatic()
    a2 = SpamStatic()
    a3 = SpamStatic()

    SpamStatic.print_instance_counter()
    SpamStatic.print_instance_counter1()
    a3.print_instance_counter1()
    print()


    print('Subclass of SpamStatic class: SpamSub')
    sa1 = SpamSub()
    sa2 = SpamSub()
    sa3 = SpamSub()

    SpamSub.print_instance_counter()
    SpamSub.print_instance_counter1()
    sa3.print_instance_counter1()
    print()


    print('Subclass of SpamStatic class: SpamSubOther')
    sao1 = SpamSubOther()
    sao2 = SpamSubOther()
    sao3 = SpamSubOther()

    SpamSubOther.print_instance_counter()
    SpamSubOther.print_instance_counter1()
    sao3.print_instance_counter1()
    print()

    '''
    results:
    Chapter32.AdvancedClassTopics]# python3 4-spam_special.py
    SpamStatic class
    Number of instances: 3
    Number of instances: 3
    Number of instances: 3

    Subclass of SpamStatic class: SpamSub           # 创建子类对象的时候，会增加父类的实例对象计数器的数值
    Extra stuff...
    Number of instances: 6
    Extra stuff...
    Number of instances: 6
    Extra stuff...
    Number of instances: 6

    Subclass of SpamStatic class: SpamSubOther
    Number of instances: 9
    Number of instances: 9
    Number of instances: 9
    '''
