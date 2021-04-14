# Coding Metaclasses
So far, we've seen how Python routes class creation calls to a metaclass, if one is specified and provided. How, though, do we actually code a metaclass that customizes type?

It turns out that you already know most of the story -- metaclasses are coded with normal Python class statements and semantics. By definition, they are simply classes that inherit from type. Their only substantial distinctions are that Python calls them automatically at the end of a class statement, and that they must adhere to the interface expected by the type superclass.

## A Basic Metaclass
Perhaps the simplest metaclass you can code is simply a subclass of type with a \_\_new\_\_ method that creates the class object by running the default version in type. A metaclass \_\_new\_\_ like this is run by the \_\_call\_\_ method inherited from type; it typically performs whatever customization is required and calls the type superclass's \_\_new\_\_ method to create and return the new class object:
> ```python
> class Meta(type):
>     def __new__(meta, classname, supers, classdict):
>         # Run by inherited type.__call__
>         return type.__new__(meta, classname, supers, classdict)
> ```

This metaclass doesn't really do anything (we might as well let the default type class create the class), but it demonstrates the way a metaclass taps into the metaclass hook to customize -- because the metaclass is called at the end of a class statement, and because the type object's \_\_call\_\_ dispatches to the \_\_new\_\_ and \_\_init\_\_ methods, code we provide in these methods can manage all the classes created from the metaclass.

Here's our example in action again, with prints added to the metaclass and the file at large to trace (again, some filenames are implied by later command-lines in this chapter):
> 
> > ```python
> > class MetaOne(type):
> >     def __new__(meta, classname, supers, classdict):
> >         print('In MetaOne.new:', meta, classname, supers, classdict, sep='\n...')
> >         return type.__new__(meta, classname, supers, classdict)
> > 
> > class Eggs:
> >     pass
> > 
> > print('making class')
> > class Spam(Eggs, metaclass=MetaOne): 			# Inherits from Eggs, instance of MetaOne
> >     data = 1 					# Class data attribute
> >     def meth(self, arg): 		# Class method attribute
> >         return self.data + arg
> > 
> > print('making instance')
> > X = Spam()
> > print('data:', X.data, X.meth(2))
> > ```
> 
> Here, Spam inherits from Eggs and is an instance of MetaOne, but X is an instance of and inherits from Spam. When this code is run with Python 3.X, notice how the metaclass is invoked at the end of the class statement, before we ever make an instance -- metaclasses are for processing classes, and classes are for processing normal instances:
> 
> > ```powershell
> > c:\code> py -3 metaclass1.py
> > making class
> > In MetaOne.new:
> > ...<class '__main__.MetaOne'>
> > ...Spam
> > ...(<class '__main__.Eggs'>,)
> > ...{'data': 1, 'meth': <function Spam.meth at 0x02A191E0>, '__module__': '__main__'}
> > making instance
> > data: 1 3
> > ```
> 

**Presentation note:** I'm truncating addresses and omitting some irrelevant built-in \_\_X\_\_ names in namespace dictionaries in this chapter for brevity, and as noted earlier am forgoing 2.X portability due to differing declaration syntax. To run in 2.X, use the class attribute form, and change print operations as desired. This example works in 2.X with the following modifications, in the file metaclass1-2x.py; notice that either Eggs or Spam must be derived from object explicitly, or else 2.X issues a warning because new-style class can't have only classic bases here -- when in doubt, use object in 2.X metaclasses clients:
> ```python
> from __future__ import print_function 			# To run the same in 2.X (only)
> class Eggs(object): 				# One of the "object" optional
> class Spam(Eggs, object):
>     __metaclass__ = MetaOne
> ```

## Customizing Construction and Initialization
Metaclasses can also tap into the \_\_init\_\_ protocol invoked by the type object's \_\_call\_\_. In general, \_\_new\_\_ creates and returns the class object, and \_\_init\_\_ initializes the already created class passed in as an argument. Metaclasses can use either or both hooks to manage the class at creation time:
> 
> > ```python
> > class MetaTwo(type):
> >     def __new__(meta, classname, supers, classdict):
> >         print('In MetaTwo.new: ', classname, supers, classdict, sep='\n...')
> >         return type.__new__(meta, classname, supers, classdict)
> >     def __init__(Class, classname, supers, classdict):
> >         print('In MetaTwo.init:', classname, supers, classdict, sep='\n...')
> >         print('...init class object:', list(Class.__dict__.keys()))
> > 
> > class Eggs:
> >     pass
> > 
> > print('making class')
> > class Spam(Eggs, metaclass=MetaTwo): 			# Inherits from Eggs, instance of MetaTwo
> >     data = 1 						# Class data attribute
> >     def meth(self, arg): 			# Class method attribute
> >         return self.data + arg
> > 
> > print('making instance')
> > X = Spam()
> > print('data:', X.data, X.meth(2))
> > ```
> 
> In this case, the class initialization method is run after the class construction method, but both run at the end of the class statement before any instances are made. Conversely, an \_\_init\_\_ in Spam would run at instance creation time, and is not affected or run by the metaclass's \_\_init\_\_:
> 
> > ```python
> > c:\code> py -3 metaclass2.py
> > making class
> > In MetaTwo.new:
> > ...Spam
> > ...(<class '__main__.Eggs'>,)
> > ...{'data': 1, 'meth': <function Spam.meth at 0x02967268>, '__module__': '__main__'}
> > In MetaTwo.init:
> > ...Spam
> > ...(<class '__main__.Eggs'>,)
> > ...{'data': 1, 'meth': <function Spam.meth at 0x02967268>, '__module__': '__main__'}
> > ...init class object: ['__qualname__', 'data', '__module__', 'meth', '__doc__']
> > making instance
> > data: 1 3
> > ```
> 

## Other Metaclass Coding Techniques
Although redefining the type superclass's \_\_new\_\_ and \_\_init\_\_ methods is the most common way to insert logic into the class object creation process with the metaclass hook, other schemes are possible.

### Using simple factory functions
For example, metaclasses need not really be classes at all. As we've learned, the class statement issues a simple call to create a class at the conclusion of its processing. Because of this, any callable object can in principle be used as a metaclass, provided it accepts the arguments passed and returns an object compatible with the intended class.

In fact, a simple object factory function may serve just as well as a type subclass:
> 
> > ```python
> > # A simple function can serve as a metaclass too
> > def MetaFunc(classname, supers, classdict):
> >     print('In MetaFunc: ', classname, supers, classdict, sep='\n...')
> >     return type(classname, supers, classdict)
> > 
> > class Eggs:
> >     pass
> > 
> > print('making class')
> > class Spam(Eggs, metaclass=MetaFunc): 				# Run simple function at end
> >     data = 1 					# Function returns class
> >     def meth(self, arg):
> >         return self.data + arg
> > 
> > print('making instance')
> > X = Spam()
> > print('data:', X.data, X.meth(2))
> > ```
> 
> When run, the function is called at the end of the declaring class statement, and it returns the expected new class object. The function is simply catching the call that the type object's \_\_call\_\_ normally intercepts by default:
> 
> > ```poweshell
> > c:\code> py -3 metaclass3.py
> > making class
> > In MetaFunc:
> > ...Spam
> > ...(<class '__main__.Eggs'>,)
> > ...{'data': 1, 'meth': <function Spam.meth at 0x029471E0>, '__module__': '__main__'}
> > making instance
> > data: 1 3
> > ```
> 

### Overloading class creation calls with normal classes
Because normal class instances can respond to call operations with operator overloading, they can serve in some metaclass roles too, much like the preceding function. The output of the following is similar to the prior class-based versions, but it's based on a simple class -- one that doesn't inherit from type at all, and provides a \_\_call\_\_ for its instances that catches the metaclass call using normal operator overloading. Note that \_\_new\_\_ and \_\_init\_\_ must have different names here, or else they will run when the Meta instance is created, not when it is later called in the role of metaclass:
> 
> > ```python
> > # A normal class instance can serve as a metaclass too
> > class MetaObj:
> >     def __call__(self, classname, supers, classdict):
> >         print('In MetaObj.call: ', classname, supers, classdict, sep='\n...')
> >         Class = self.__New__(classname, supers, classdict)
> >         self.__Init__(Class, classname, supers, classdict)
> >         return Class
> > 
> >     def __New__(self, classname, supers, classdict):
> >         print('In MetaObj.new: ', classname, supers, classdict, sep='\n...')
> >         return type(classname, supers, classdict)
> > 
> >     def __Init__(self, Class, classname, supers, classdict):
> >         print('In MetaObj.init:', classname, supers, classdict, sep='\n...')
> >         print('...init class object:', list(Class.__dict__.keys()))
> > 
> > class Eggs:
> >     pass
> > 
> > print('making class')
> > class Spam(Eggs, metaclass=MetaObj()): 				# MetaObj is normal class instance
> >     data = 1 					# Called at end of statement
> >     def meth(self, arg):
> >         return self.data + arg
> > 
> > print('making instance')
> > X = Spam()
> > print('data:', X.data, X.meth(2))
> > ```
> 
> When run, the three methods are dispatched via the normal instance's \_\_call\_\_ inherited from its normal class, but without any dependence on type dispatch mechanics or semantics:
> 
> > ```python
> > c:\code> py -3 metaclass4.py
> > making class
> > In MetaObj.call:
> > ...Spam
> > ...(<class '__main__.Eggs'>,)
> > ...{'data': 1, 'meth': <function Spam.meth at 0x029492F0>, '__module__': '__main__'}
> > In MetaObj.new:
> > ...Spam
> > ...(<class '__main__.Eggs'>,)
> > ...{'data': 1, 'meth': <function Spam.meth at 0x029492F0>, '__module__': '__main__'}
> > In MetaObj.init:
> > ...Spam
> > ...(<class '__main__.Eggs'>,)
> > ...{'data': 1, 'meth': <function Spam.meth at 0x029492F0>, '__module__': '__main__'}
> > ...init class object: ['__module__', '__doc__', 'data', '__qualname__', 'meth']
> > making instance
> > data: 1 3
> > ```
> 

In fact, we can use normal superclass inheritance to acquire the call interceptor in this coding model -- the superclass here is serving essentially the same role as type, at least in terms of metaclass dispatch:
> 
> > ```python
> > # Instances inherit from classes and their supers normally
> > class SuperMetaObj:
> >     def __call__(self, classname, supers, classdict):
> >         print('In SuperMetaObj.call: ', classname, supers, classdict, sep='\n...')
> >         Class = self.__New__(classname, supers, classdict)
> >         self.__Init__(Class, classname, supers, classdict)
> >         return Class
> > 
> > class SubMetaObj(SuperMetaObj):
> >     def __New__(self, classname, supers, classdict):
> >         print('In SubMetaObj.new: ', classname, supers, classdict, sep='\n...')
> >         return type(classname, supers, classdict)
> > 
> >     def __Init__(self, Class, classname, supers, classdict):
> >         print('In SubMetaObj.init:', classname, supers, classdict, sep='\n...')
> >         print('...init class object:', list(Class.__dict__.keys()))
> > 
> > class Spam(Eggs, metaclass=SubMetaObj()): 			# Invoke Sub instance via Super.__call__
> >     ...rest of file unchanged...
> > ```
> 
> Execute in cmd: 
> 
> > ```powershell
> > c:\code> py -3 metaclass4-super.py
> > making class
> > In SuperMetaObj.call:
> > ...as before...
> > In SubMetaObj.new:
> > ...as before...
> > In SubMetaObj.init:
> > ...as before...
> > making instance
> > data: 1 3
> > ```
> 

Although such alternative forms work, most metaclasses get their work done by redefining the type superclass's \_\_new\_\_ and \_\_init\_\_; in practice, this is usually as much control as is required, and it's often simpler than other schemes. Moreover, metaclasses have access to additional tools, such as class methods we'll explore ahead, which can influence class behavior more directly than some other schemes.

Still, we'll see later that a simple callable-based metaclass can often work much like a class decorator, which allows the metaclasses to manage instances as well as classes.

First, though, the next section presents an example drawn from the Python "Twilight Zone" to introduce metaclass name resolution concepts.

### Overloading class creation calls with metaclasses
Since they participate in normal OOP mechanics, it's also possible for metaclasses to catch the creation call at the end of a class statement directly, by redefining the type object's \_\_call\_\_. The redefinitions of both \_\_new\_\_ and \_\_call\_\_ must be careful to call back to their defaults in type if they mean to make a class in the end, and \_\_call\_\_ must invoke type to kick off the other two here:
> 
> > ```
> > # Classes can catch calls too (but built-ins look in metas, not supers!)
> > class SuperMeta(type):
> >     def __call__(meta, classname, supers, classdict):
> >         print('In SuperMeta.call: ', classname, supers, classdict, sep='\n...')
> >         return type.__call__(meta, classname, supers, classdict)
> > 
> >     def __init__(Class, classname, supers, classdict):
> >         print('In SuperMeta init:', classname, supers, classdict, sep='\n...')
> >         print('...init class object:', list(Class.__dict__.keys()))
> > 
> > print('making metaclass')
> > class SubMeta(type, metaclass=SuperMeta):
> >     def __new__(meta, classname, supers, classdict):
> >         print('In SubMeta.new: ', classname, supers, classdict, sep='\n...')
> >         return type.__new__(meta, classname, supers, classdict)
> > 
> >     def __init__(Class, classname, supers, classdict):
> >         print('In SubMeta init:', classname, supers, classdict, sep='\n...')
> >         print('...init class object:', list(Class.__dict__.keys()))
> > 
> > class Eggs:
> >     pass
> > 
> > print('making class')
> > class Spam(Eggs, metaclass=SubMeta): 			# Invoke SubMeta, via SuperMeta.__call__
> >     data = 1
> >     def meth(self, arg):
> >         return self.data + arg
> > 
> > print('making instance')
> > X = Spam()
> > print('data:', X.data, X.meth(2))
> > ```
> 
> This code has some oddities I'll explain in a moment. When run, though, all three redefined methods run in turn for Spam as in the prior section. This is again essentially what the type object does by default, but there's an additional metaclass call for the metaclass subclass (metasubclass?):
> 
> > ```powershell
> > c:\code> py -3 metaclass5.py
> > making metaclass
> > In SuperMeta init:
> > ...SubMeta
> > ...(<class 'type'>,)
> > ...{'__init__': <function SubMeta.__init__ at 0x028F92F0>, ...}
> > ...init class object: ['__doc__', '__module__', '__new__', '__init__, ...]
> > making class
> > In SuperMeta.call:
> > ...Spam
> > ...(<class '__main__.Eggs'>,)
> > ...{'data': 1, 'meth': <function Spam.meth at 0x028F9378>, '__module__': '__main__'}
> > In SubMeta.new:
> > ...Spam
> > ...(<class '__main__.Eggs'>,)
> > ...{'data': 1, 'meth': <function Spam.meth at 0x028F9378>, '__module__': '__main__'}
> > In SubMeta init:
> > ...Spam
> > ...(<class '__main__.Eggs'>,)
> > ...{'data': 1, 'meth': <function Spam.meth at 0x028F9378>, '__module__': '__main__'}
> > ...init class object: ['__qualname__', '__module__', '__doc__', 'data', 'meth']
> > making instance
> > data: 1 3
> > ```
> 

This example is complicated by the fact that it overrides a method invoked by a builtin operation -- in this case, the call run automatically to create a class. Metaclasses are used to create class objects, but only generate instances of themselves when called in a metaclass role. Because of this, name lookup with metaclasses may be somewhat different than what we are accustomed to. The \_\_call\_\_ method, for example, is looked up by built-ins in the class (a.k.a. type) of an object; for metaclasses, this means the metaclass of a metaclass!

As we'll see ahead, metaclasses also inherit names from other metaclasses normally, but as for normal classes, this seems to apply to explicit name fetches only, not to the implicit lookup of names for built-in operations such as calls. The latter appears to look in the metaclass's class, available in its \_\_class\_\_ link -- which is either the default type or a metaclass. This is the same built-ins routing issue we've seen so often in this book for normal class instances. The metaclass in SubMeta is required to set this link, though this also kicks off a metaclass construction step for the metaclass itself.

Trace the invocations in the output. SuperMeta's \_\_call\_\_ method is not run for the call to SuperMeta when making SubMeta (this goes to type instead), but is run for the SubMeta call when making Spam. Inheriting normally from SuperMeta does not suffice to catch SubMeta calls, and for reasons we'll see later is actually the wrong thing to do for operator overloading methods: SuperMeta's \_\_call\_\_ is then acquired by Spam, causing Spam instance creation calls to fail before any instance is ever created. Subtle but true!

Here's an illustration of the issue in simpler terms -- a normal superclass is skipped for built-ins, but not for explicit fetches and calls, the latter relying on normal attribute name inheritance:
> 
> > ```python
> > class SuperMeta(type):
> >     def __call__(meta, classname, supers, classdict): 			# By name, not built-in
> >         print('In SuperMeta.call:', classname)
> >         return type.__call__(meta, classname, supers, classdict)
> > 
> > class SubMeta(SuperMeta): 					# Created by type default
> >     def __init__(Class, classname, supers, classdict): 			# Overrides type.__init__
> >         print('In SubMeta init:', classname)
> > 
> > print(SubMeta.__class__)
> > print([n.__name__ for n in SubMeta.__mro__])
> > print()
> > print(SubMeta.__call__) 					# Not a data descriptor if found by name
> > print()
> > SubMeta.__call__(SubMeta, 'xxx', (), {}) 	# Explicit calls work: class inheritance
> > print()
> > SubMeta('yyy', (), {}) 						# But implicit built-in calls do not: type
> > ```
>  
> > execute in cmd:
>  
> > ```powershell
> > c:\code> py -3 metaclass5b.py
> > <class 'type'>
> > ['SubMeta', 'SuperMeta', 'type', 'object']
> > <function SuperMeta.__call__ at 0x029B9158>
> > In SuperMeta.call: xxx
> > In SubMeta init: xxx
> > In SubMeta init: yyy
> > ```
> 

Of course, this specific example is a special case: catching a built-in run on a metaclass, a likely rare usage related to \_\_call\_\_ here. But it underscores a core asymmetry and apparent inconsistency: normal attribute inheritance is not fully used for built-in dispatch -- for both instances and classes.

To truly understand this example's subtleties, though, we need to get more formal about what metaclasses mean for Python name resolution in general.

