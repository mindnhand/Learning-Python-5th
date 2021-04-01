# Example: Attribute Validations
To close out this chapter, let's turn to a more realistic example, coded in all four of our attribute management schemes. The example we will use defines a CardHolder object with four attributes, three of which are managed. The managed attributes validate or transform values when fetched or stored. All four versions produce the same results for the same test code, but they implement their attributes in very different ways. The examples are included largely for self-study; although I won't go through their code in detail, they all use concepts we've already explored in this chapter.

## Using Properties to Validate
Our first coding in the file that follows uses properties to manage three attributes. As usual, we could use simple methods instead of managed attributes, but properties help if we have been using attributes in existing code already. Properties run code automatically on attribute access, but are focused on a specific set of attributes; they cannot be used to intercept all attributes generically.

To understand this code, it's crucial to notice that the attribute assignments inside the \_\_init\_\_ constructor method trigger property setter methods too. When this method assigns to self.name, for example, it automatically invokes the setName method, which transforms the value and assigns it to an instance attribute called \_\_name so it won't clash with the property's name.

This renaming (sometimes called name mangling) is necessary because properties use common instance state and have none of their own. Data is stored in an attribute called \_\_name, and the attribute called name is always a property, not data. As we saw in Chapter 31, names like \_\_name are known as pseudoprivate attributes, and are changed by Python to include the enclosing class's name when stored in the instance's namespace; here, this helps keep the implementation-specific attributes distinct from others, including that of the property that manages them.

In the end, this class manages attributes called name, age, and acct; allows the attribute addr to be accessed directly; and provides a read-only attribute called remain that is entirely virtual and computed on demand. For comparison purposes, this propertybased coding weighs in at 39 lines of code, not counting its two initial lines, and includes the object derivation required in 2.X but optional in 3.X:
> ```python
> # File validate_properties.py
> class CardHolder(object): 			# Need "(object)" for setter in 2.X
>     acctlen = 8 				# Class data
>     retireage = 59.5
>     def __init__(self, acct, name, age, addr):
>         self.acct = acct 			# Instance data
>         self.name = name 			# These trigger prop setters too!
>         self.age = age 			# __X mangled to have class name
>         self.addr = addr 			# addr is not managed
>         							# remain has no data
>     def getName(self):
>         return self.__name
>     def setName(self, value):
>         value = value.lower().replace(' ', '_')
>         self.__name = value
>     name = property(getName, setName)
> 
>     def getAge(self):
>         return self.__age
>     def setAge(self, value):
>         if value < 0 or value > 150:
>             raise ValueError('invalid age')
>         else:
>             self.__age = value
>     age = property(getAge, setAge)
> 
>     def getAcct(self):
>         return self.__acct[:-3] + '***'
>     def setAcct(self, value):
>         value = value.replace('-', '')
>         if len(value) != self.acctlen:
>             raise TypeError('invald acct number')
>         else:
>             self.__acct = value
>     acct = property(getAcct, setAcct)
> 
>     def remainGet(self): 			# Could be a method, not attr
>         return self.retireage - self.age 			# Unless already using as attr
>     remain = property(remainGet)
> ```

### Testing code
The following code, validate\_tester.py, tests our class; run this script with the name of the class's module (sans ".py") as a single command-line argument (you could also add most of its test code to the bottom of each file, or interactively import it from a module after importing the class). We'll use this same testing code for all four versions of this example. When it runs, it makes two instances of our managed-attribute class and fetches and changes their various attributes. Operations expected to fail are wrapped in try statements, and identical behavior on 2.X is supported by enabling the 3.X print function:
> 
> > ```python
> > # File validate_tester.py
> > from __future__ import print_function 			# 2.X
> > def loadclass():
> >     import sys, importlib
> >     modulename = sys.argv[1] 						# Module name in command line
> >     module = importlib.import_module(modulename) 	# Import module by name string
> >     print('[Using: %s]' % module.CardHolder) 		# No need for getattr() here
> >     return module.CardHolder
> > 
> > def printholder(who):
> >     print(who.acct, who.name, who.age, who.remain, who.addr, sep=' / ')
> > 
> > if __name__ == '__main__':
> >     CardHolder = loadclass()
> >     bob = CardHolder('1234-5678', 'Bob Smith', 40, '123 main st')
> >     printholder(bob)
> >     bob.name = 'Bob Q. Smith'
> >     bob.age = 50
> >     bob.acct = '23-45-67-89'
> >     printholder(bob)
> >     sue = CardHolder('5678-12-34', 'Sue Jones', 35, '124 main st')
> >     printholder(sue)
> >     try:
> >         sue.age = 200
> >     except:
> >         print('Bad age for Sue')
> >     try:
> >         sue.remain = 5
> >     except:
> >         print("Can't set sue.remain")
> >     try:
> >         sue.acct = '1234567'
> >     except:
> >         print('Bad acct for Sue')
> > ```
> 
> Here is the output of our self-test code on both Python 3.X and 2.X; again, this is the same for all versions of this example, except for the tested class's name. Trace through this code to see how the class's methods are invoked; accounts are displayed with some digits hidden, names are converted to a standard format, and time remaining until retirement is computed when fetched using a class attribute cutoff:
> 
> > ```powershell
> > c:\code> py -3 validate_tester.py validate_properties
> > [Using: <class 'validate_properties.CardHolder'>]
> > 12345*** / bob_smith / 40 / 19.5 / 123 main st
> > 23456*** / bob_q._smith / 50 / 9.5 / 123 main st
> > 56781*** / sue_jones / 35 / 24.5 / 124 main st
> > Bad age for Sue
> > Can't set sue.remain
> > Bad acct for Sue
> > ```
> 

## Using Descriptors to Validate
Now, let's recode our example using descriptors instead of properties. As we've seen, descriptors are very similar to properties in terms of functionality and roles; in fact, properties are basically a restricted form of descriptor. Like properties, descriptors are designed to handle specific attributes, not generic attribute access. Unlike properties, descriptors can also have their own state, and are a more general scheme.

### Option 1: Validating with shared descriptor instance state
To understand the following code, it's again important to notice that the attribute assignments inside the \_\_init\_\_ constructor method trigger descriptor \_\_set\_\_ methods. When the constructor method assigns to self.name, for example, it automatically invokes the Name.\_\_set\_\_() method, which transforms the value and assigns it to a descriptor attribute called name.

In the end, this class implements the same attributes as the prior version: it manages attributes called name, age, and acct; allows the attribute addr to be accessed directly; and provides a read-only attribute called remain that is entirely virtual and computed on demand. Notice how we must catch assignments to the remain name in its descriptor and raise an exception; as we learned earlier, if we did not do this, assigning to this attribute of an instance would silently create an instance attribute that hides the class attribute descriptor.

For comparison purposes, this descriptor-based coding takes 45 lines of code; I've added the required object derivation to the main descriptor classes for 2.X compatibility (they can be omitted for code to be run in 3.X only, but don't hurt in 3.X, and aid portability if present):
> 
> > ```python
> > # File validate_descriptors1.py: using shared descriptor state
> > class CardHolder(object): 			# Need all "(object)" in 2.X only
> >     acctlen = 8 					# Class data
> >     retireage = 59.5
> >     def __init__(self, acct, name, age, addr):
> >         self.acct = acct 			# Instance data
> >         self.name = name 			# These trigger __set__ calls too!
> >         self.age = age 				# __X not needed: in descriptor
> >         self.addr = addr 			# addr is not managed
> >         							# remain has no data
> > 
> >     class Name(object):
> >         def __get__(self, instance, owner): 		# Class names: CardHolder locals
> >             return self.name
> >         def __set__(self, instance, value):
> >             value = value.lower().replace(' ', '_')
> >             self.name = value
> >     name = Name()
> > 
> >     class Age(object):
> >         def __get__(self, instance, owner):
> >             return self.age 			# Use descriptor data
> >         def __set__(self, instance, value):
> >             if value < 0 or value > 150:
> >                 raise ValueError('invalid age')
> >             else:
> >                 self.age = value
> >     age = Age()
> > 
> >     class Acct(object):
> >         def __get__(self, instance, owner):
> >             return self.acct[:-3] + '***'
> >         def __set__(self, instance, value):
> >             value = value.replace('-', '')
> >             if len(value) != instance.acctlen: 		# Use instance class data
> >                 raise TypeError('invald acct number')
> >             else:
> >                 self.acct = value
> >     acct = Acct()
> > 
> >     class Remain(object):
> >         def __get__(self, instance, owner):
> >             return instance.retireage - instance.age 	# Triggers Age.__get__
> >         def __set__(self, instance, value):
> >             raise TypeError('cannot set remain') 		# Else set allowed here
> >     remain = Remain()
> > ```
> 
> When run with the prior testing script, all examples in this section produce the same output as shown for properties earlier, except that the name of the class in the first line varies:
> 
> > ```powershell
> > C:\code> python validate_tester.py validate_descriptors1
> > ...same output as properties, except class name...
> > ```
> 

### Option 2: Validating with per-client-instance state
Unlike in the prior property-based variant, though, in this case the actual name value is attached to the descriptor object, not the client class instance. Although we could store this value in either instance or descriptor state, the latter avoids the need to mangle names with underscores to avoid collisions. In the CardHolder client class, the attribute called name is always a descriptor object, not data.

Importantly, the downside of this scheme is that state stored inside a descriptor itself is class-level data that is effectively shared by all client class instances, and so cannot vary between them. That is, storing state in the descriptor instance instead of the owner (client) class instance means that the state will be the same in all owner class instances. Descriptor state can vary only per attribute appearance.

To see this at work, in the preceding descriptor-based CardHolder example, try printing attributes of the bob instance after creating the second instance, sue. The values of sue's managed attributes (name, age, and acct) overwrite those of the earlier object bob, because both share the same, single descriptor instance attached to their class:
> 
> > ```python
> > # File validate_tester2.py
> > from __future__ import print_function 			# 2.X
> > from validate_tester import loadclass
> > CardHolder = loadclass()
> > bob = CardHolder('1234-5678', 'Bob Smith', 40, '123 main st')
> > print('bob:', bob.name, bob.acct, bob.age, bob.addr)
> > sue = CardHolder('5678-12-34', 'Sue Jones', 35, '124 main st')
> > print('sue:', sue.name, sue.acct, sue.age, sue.addr) 		# addr differs: client data
> > print('bob:', bob.name, bob.acct, bob.age, bob.addr) 		# name,acct,age overwritten?
> > ```
> 
> The results confirm the suspicion -- in terms of managed attributes, bob has morphed into sue!
> 
> > ```powershell
> > c:\code> py −3 validate_tester2.py validate_descriptors1
> > [Using: <class 'validate_descriptors1.CardHolder'>]
> > bob: bob_smith 12345*** 40 123 main st
> > sue: sue_jones 56781*** 35 124 main st
> > bob: sue_jones 56781*** 35 123 main st
> > ```
> 
There are valid uses for descriptor state, of course -- to manage descriptor implementation and data that spans all instance -- and this code was implemented to illustrate the technique. Moreover, the state scope implications of class versus instance attributes should be more or less a given at this point in the book.

However, in this particular use case, attributes of CardHolder objects are probably better stored as per-instance data instead of descriptor instance data, perhaps using the same \_\_X naming convention as the property-based equivalent to avoid name clashes in the instance -- a more important factor this time, as the client is a different class with its own state attributes. Here are the required coding changes; it doesn’t change line counts (we're still at 45):
> 
> > ```python
> > # File validate_descriptors2.py: using per-client-instance state
> > class CardHolder(object): 				# Need all "(object)" in 2.X only
> >     acctlen = 8 						# Class data
> >     retireage = 59.5
> >     def __init__(self, acct, name, age, addr):
> >         self.acct = acct 				# Client instance data
> >         self.name = name 				# These trigger __set__ calls too!
> >         self.age = age 					# __X needed: in client instance
> >         self.addr = addr 				# addr is not managed
> >         								# remain managed but has no data
> >     class Name(object):
> >         def __get__(self, instance, owner): 		# Class names: CardHolder locals
> >             return instance.__name
> >         def __set__(self, instance, value):
> >             value = value.lower().replace(' ', '_')
> >             instance.__name = value
> >     name = Name() 					# class.name vs mangled attr
> > 
> >     class Age(object):
> >         def __get__(self, instance, owner):
> >             return instance.__age 		# Use descriptor data
> >         def __set__(self, instance, value):
> >             if value < 0 or value > 150:
> >                 raise ValueError('invalid age')
> >             else:
> >                 instance.__age = value
> >     age = Age() 				# class.age vs mangled attr
> > 
> >     class Acct(object):
> >         def __get__(self, instance, owner):
> >             return instance.__acct[:-3] + '***'
> >         def __set__(self, instance, value):
> >             value = value.replace('-', '')
> >             if len(value) != instance.acctlen: 			# Use instance class data
> >                 raise TypeError('invald acct number')
> >             else:
> >                 instance.__acct = value
> >     acct = Acct() 			# class.acct vs mangled name
> >  
> >     class Remain(object):
> >         def __get__(self, instance, owner):
> >             return instance.retireage - instance.age 		# Triggers Age.__get__
> >         def __set__(self, instance, value):
> >             raise TypeError('cannot set remain') 			# Else set allowed here
> >     remain = Remain()
> > ```
> 
> This supports per-instance data for the name, age, and acct managed fields as expected (bob remains bob), and other tests work as before:
> 
> > ```powershell
> > c:\code> py -3 validate_tester2.py validate_descriptors2
> > [Using: <class 'validate_descriptors2.CardHolder'>]
> > bob: bob_smith 12345*** 40 123 main st
> > sue: sue_jones 56781*** 35 124 main st
> > bob: bob_smith 12345*** 40 123 main st
> > c:\code> py −3 validate_tester.py validate_descriptors2
> > ...same output as properties, except class name...
> > ```
> 

One small caveat here: as coded, this version doesn't support through-class descriptor access, because such access passes a None to the instance argument (also notice the attribute \_\_X name mangling to \_Name\_\_name in the error message when the fetch attempt is made):
> ```python
> >>> from validate_descriptors1 import CardHolder
> >>> bob = CardHolder('1234-5678', 'Bob Smith', 40, '123 main st')
> >>> bob.name
> 'bob_smith'
> >>> CardHolder.name
> 'bob_smith'
> >>> from validate_descriptors2 import CardHolder
> >>> bob = CardHolder('1234-5678', 'Bob Smith', 40, '123 main st')
> >>> bob.name
> 'bob_smith'
> >>> CardHolder.name
> AttributeError: 'NoneType' object has no attribute '_Name__name'
> ```

We could detect this with a minor amount of additional code to trigger the error more explicitly, but there's probably no point -- because this version stores data in the client instance, there's no meaning to its descriptors unless they're accompanied by a client instance (much like a normal unbound instance method). In fact, that's really the entire point of this version's change!

Because they are classes, descriptors are a useful and powerful tool, but they present choices that can deeply impact a program's behavior. As always in OOP, choose your state retention policies carefully.

## Using \_\_getattr\_\_ to Validate
As we've seen, the \_\_getattr\_\_ method intercepts all undefined attributes, so it can be more generic than using properties or descriptors. For our example, we simply test the attribute name to know when a managed attribute is being fetched; others are stored physically on the instance and so never reach \_\_getattr\_\_. Although this approach is more general than using properties or descriptors, extra work may be required to imitate the specific-attribute focus of other tools. We need to check names at runtime, and we must code a \_\_setattr\_\_ in order to intercept and validate attribute assignments.

As for the property and descriptor versions of this example, it's critical to notice that the attribute assignments inside the \_\_init\_\_ constructor method trigger the class's \_\_setattr\_\_ method too. When this method assigns to self.name, for example, it automatically invokes the \_\_setattr\_\_ method, which transforms the value and assigns it to an instance attribute called name. By storing name on the instance, it ensures that future accesses will not trigger \_\_getattr\_\_. In contrast, acct is stored as \_acct, so that later accesses to acct do invoke \_\_getattr\_\_.

In the end, this class, like the prior two, manages attributes called name, age, and acct; allows the attribute addr to be accessed directly; and provides a read-only attribute called remain that is entirely virtual and is computed on demand.

For comparison purposes, this alternative comes in at 32 lines of code -- 7 fewer than the property-based version, and 13 fewer than the version using descriptors. Clarity matters more than code size, of course, but extra code can sometimes imply extra development and maintenance work. Probably more important here are roles: generic tools like \_\_getattr\_\_ may be better suited to generic delegation, while properties and descriptors are more directly designed to manage specific attributes.

Also note that the code here incurs extra calls when setting unmanaged attributes (e.g., addr), although no extra calls are incurred for fetching unmanaged attributes, since they are defined. Though this will likely result in negligible overhead for most programs, the more narrowly focused properties and descriptors incur an extra call only when managed attributes are accessed, and also appear in dir results when needed by generic tools. Here's the \_\_getattr\_\_ version of our validations code:
> 
> > ```python
> > # File validate_getattr.py
> > class CardHolder:
> >     acctlen = 8 				# Class data
> >     retireage = 59.5
> >     def __init__(self, acct, name, age, addr):
> >         self.acct = acct 			# Instance data
> >         self.name = name 			# These trigger __setattr__ too
> >         self.age = age 				# _acct not mangled: name tested
> >         self.addr = addr 			# addr is not managed
> >         							# remain has no data
> > 
> >     def __getattr__(self, name):
> >         if name == 'acct': 			# On undefined attr fetches
> >             return self._acct[:-3] + '***' 			# name, age, addr are defined
> >         elif name == 'remain':
> >             return self.retireage - self.age 		# Doesn't trigger __getattr__
> >         else:
> >             raise AttributeError(name)
> >     def __setattr__(self, name, value):
> >         if name == 'name': 			# On all attr assignments
> >             value = value.lower().replace(' ', '_') 	# addr stored directly
> >         elif name == 'age': 			# acct mangled to _acct
> >             if value < 0 or value > 150:
> >                 raise ValueError('invalid age')
> >         elif name == 'acct':
> >             name = '_acct'
> >             value = value.replace('-', '')
> >             if len(value) != self.acctlen:
> >                 raise TypeError('invald acct number')
> >         elif name == 'remain':
> >             raise TypeError('cannot set remain')
> >         self.__dict__[name] = value 			# Avoid looping (or via object)
> > ```
> 
> When this code is run with either test script, it produces the same output (with a different class name):
> 
> > ```powershell
> > c:\code> py −3 validate_tester.py validate_getattr
> > ...same output as properties, except class name...
> > c:\code> py −3 validate_tester2.py validate_getattr
> > ...same output as instance-state descriptors, except class name...
> > ```
> 

## Using \_\_getattribute\_\_ to Validate
Our final variant uses the \_\_getattribute\_\_ catchall to intercept attribute fetches and manage them as needed. Every attribute fetch is caught here, so we test the attribute names to detect managed attributes and route all others to the superclass for normal fetch processing. This version uses the same \_\_setattr\_\_ to catch assignments as the prior version.

The code works very much like the \_\_getattr\_\_ version, so I won't repeat the full description here. Note, though, that because every attribute fetch is routed to \_\_getattribute\_\_, we don't need to mangle names to intercept them here (acct is stored as acct). On the other hand, this code must take care to route nonmanaged attribute fetches to a superclass to avoid looping or extra calls.

Also notice that this version incurs extra calls for both setting and fetching unmanaged attributes (e.g., addr); if speed is paramount, this alternative may be the slowest of the bunch. For comparison purposes, this version amounts to 32 lines of code, just like the prior version, and includes the requisite object derivation for 2.X compatibility; like properties and descriptors, \_\_getattribute\_\_ is a new-style class tool:
> ```python
> # File validate_getattribute.py
> class CardHolder(object): 			# Need "(object)" in 2.X only
>     acctlen = 8 						# Class data
>     retireage = 59.5
>     def __init__(self, acct, name, age, addr):
>         self.acct = acct 				# Instance data
>         self.name = name 				# These trigger __setattr__ too
>         self.age = age 				# acct not mangled: name tested
>         self.addr = addr 				# addr is not managed
>     def __getattribute__(self, name):
>         superget = object.__getattribute__ 		# Don't loop: one level up
>         if name == 'acct': 			# On all attr fetches
>             return superget(self, 'acct')[:-3] + '***'
>         elif name == 'remain':
>             return superget(self, 'retireage') - superget(self, 'age')
>         else:
>             return superget(self, name) 		# name, age, addr: stored
>     def __setattr__(self, name, value):
>         if name == 'name': 			# On all attr assignments
>             value = value.lower().replace(' ', '_') 		# addr stored directly
>         elif name == 'age':
>             if value < 0 or value > 150:
>                 raise ValueError('invalid age')
>         elif name == 'acct':
>             value = value.replace('-', '')
>             if len(value) != self.acctlen:
>                 raise TypeError('invald acct number')
>         elif name == 'remain':
>             raise TypeError('cannot set remain')
>         self.__dict__[name] = value 	# Avoid loops, orig names
> ```

Both the getattr and getattribute scripts work the same as the property and per-clientinstance descriptor versions, when run by both tester scripts on either 2.X or 3.X. -- four ways to achieve the same goal in Python, though they vary in structure, and are perhaps less redundant in some other roles. Be sure to study and run this section's code on your own for more pointers on managed attribute coding techniques.

